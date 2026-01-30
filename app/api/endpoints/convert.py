"""Conversion API endpoint."""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import time
from typing import Optional
from app.core.config import settings
from app.models.schemas import ConversionResponse
from app.services.pdf_processor import PDFProcessor
from app.services.docx_generator import DOCXGenerator

router = APIRouter()


async def cleanup_file(file_path: Path):
    """Background task to delete file after delay."""
    import asyncio
    await asyncio.sleep(settings.file_ttl_hours * 3600)
    if file_path.exists():
        file_path.unlink()


@router.post("/convert", response_model=ConversionResponse)
async def convert_pdf_to_docx(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    preserve_fonts: bool = True,
    extract_images: bool = True,
):
    """
    Convert PDF to DOCX with layout preservation.
    
    Args:
        file: PDF file to convert
        preserve_fonts: Attempt to preserve original fonts
        extract_images: Extract images from PDF
        
    Returns:
        Conversion response with file_id and download URL
    """
    start_time = time.time()
    
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Save uploaded PDF temporarily
    upload_path = settings.upload_dir / f"{file_id}.pdf"
    with open(upload_path, "wb") as f:
        f.write(file_content)
    
    try:
        # Process PDF
        processor = PDFProcessor(upload_path)
        pages = processor.process_all_pages()
        
        # Generate DOCX
        output_path = settings.output_dir / f"{file_id}.docx"
        generator = DOCXGenerator()
        generator.create_document(pages, output_path)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Schedule cleanup of both files
        background_tasks.add_task(cleanup_file, upload_path)
        background_tasks.add_task(cleanup_file, output_path)
        
        return ConversionResponse(
            file_id=file_id,
            status="completed",
            message="PDF successfully converted to DOCX",
            download_url=f"/api/download/{file_id}",
            pages_processed=len(pages),
            processing_time_seconds=round(processing_time, 2),
        )
    
    except Exception as e:
        # Cleanup on error
        if upload_path.exists():
            upload_path.unlink()
        
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.get("/download/{file_id}")
async def download_converted_file(file_id: str):
    """
    Download converted DOCX file.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        DOCX file for download
    """
    file_path = settings.output_dir / f"{file_id}.docx"
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found or has expired (files auto-delete after 1 hour)"
        )
    
    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"converted_{file_id}.docx",
    )
