"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional


class ConversionResponse(BaseModel):
    """Response model for PDF conversion."""
    
    file_id: str = Field(..., description="Unique identifier for the converted file")
    status: str = Field(..., description="Conversion status: processing, completed, failed")
    message: Optional[str] = Field(None, description="Status message or error details")
    download_url: Optional[str] = Field(None, description="URL to download converted file")
    pages_processed: Optional[int] = Field(None, description="Number of pages processed")
    processing_time_seconds: Optional[float] = Field(None, description="Processing duration")


class ConversionRequest(BaseModel):
    """Request model for PDF conversion options."""
    
    preserve_fonts: bool = Field(True, description="Attempt to preserve original fonts")
    extract_images: bool = Field(True, description="Extract images from PDF (lossless)")
    preserve_layout: bool = Field(True, description="Preserve original layout structure")
    

class FileInfo(BaseModel):
    """File information model."""
    
    filename: str
    size_bytes: int
    pages: int
    has_text: bool
    has_images: bool
