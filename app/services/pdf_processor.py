"""PDF processing service using pdfplumber and PyMuPDF."""

import pdfplumber
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from app.services.font_mapper import FontMapper

try:
    from app.services.ocr_processor import OCRProcessor
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


@dataclass
class PDFTextBlock:
    """Represents a text block extracted from PDF."""
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font_name: str
    font_size: float
    

@dataclass
class PDFImage:
    """Represents an image extracted from PDF."""
    data: bytes
    width: int
    height: int
    dpi: int
    format: str  # png, jpeg, etc.
    position: tuple[float, float, float, float]  # x0, y0, x1, y1


@dataclass
class PDFPage:
    """Represents a processed PDF page."""
    page_number: int
    text_blocks: List[PDFTextBlock]
    images: List[PDFImage]
    width: float
    height: float
    has_text: bool
    has_images: bool


class PDFProcessor:
    """Handles PDF parsing and content extraction."""
    
    def __init__(self, pdf_path: Path, enable_ocr: bool = True, ocr_languages: Optional[List[str]] = None):
        """
        Initialize PDF processor.
        
        Args:
            pdf_path: Path to PDF file
            enable_ocr: Enable OCR for scanned PDFs
            ocr_languages: Language codes for OCR (e.g., ['chi_sim', 'eng'])
        """
        self.pdf_path = pdf_path
        self.font_mapper = FontMapper()
        self.enable_ocr = enable_ocr and OCR_AVAILABLE
        
        if self.enable_ocr:
            self.ocr_processor = OCRProcessor(languages=ocr_languages)
        else:
            self.ocr_processor = None
    
    def get_page_count(self) -> int:
        """Get total number of pages in PDF."""
        with pdfplumber.open(self.pdf_path) as pdf:
            return len(pdf.pages)
    
    def extract_text_blocks(self, page_number: int = 0) -> List[PDFTextBlock]:
        """
        Extract text blocks from a specific page.
        Falls back to OCR if no text found (scanned PDF).
        
        Args:
            page_number: Zero-indexed page number
            
        Returns:
            List of text blocks with position and font info
        """
        text_blocks = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            if page_number >= len(pdf.pages):
                return text_blocks
            
            page = pdf.pages[page_number]
            
            # Extract words with details
            words = page.extract_words(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=False,
                use_text_flow=True,
            )
            
            for word in words:
                text_block = PDFTextBlock(
                    text=word.get("text", ""),
                    x0=word.get("x0", 0),
                    y0=word.get("y0", 0),
                    x1=word.get("x1", 0),
                    y1=word.get("y1", 0),
                    font_name=word.get("fontname", "Arial"),
                    font_size=word.get("height", 12),  # Approximate font size
                )
                text_blocks.append(text_block)
        
        # NEW V2: OCR fallback for scanned pages
        if len(text_blocks) == 0 and self.enable_ocr and self.ocr_processor:
            print(f"[V2-OCR] No text found on page {page_number}, applying OCR...")
            images = self.extract_images(page_number)
            if images:
                # Use largest image (usually the full page scan)
                largest_image = max(images, key=lambda img: img.width * img.height)
                text_blocks = self.ocr_processor.extract_text_from_image(
                    largest_image.data,
                    page_number
                )
        
        return text_blocks
    
    def extract_images(self, page_number: int = 0) -> List[PDFImage]:
        """
        Extract images from PDF using PyMuPDF (lossless).
        
        Args:
            page_number: Zero-indexed page number
            
        Returns:
            List of images with metadata
        """
        images = []
        
        doc = fitz.open(self.pdf_path)
        
        if page_number >= len(doc):
            doc.close()
            return images
        
        page = doc[page_number]
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            
            # Get image position (bounding box)
            # Note: This is a simplified approach
            # In production, you'd need more sophisticated positioning
            rect = page.get_image_bbox(img_info)
            
            pdf_image = PDFImage(
                data=base_image["image"],
                width=base_image["width"],
                height=base_image["height"],
                dpi=72,  # Default PDF DPI, calculate actual DPI if needed
                format=base_image["ext"],
                position=(rect.x0, rect.y0, rect.x1, rect.y1) if rect else (0, 0, 0, 0),
            )
            images.append(pdf_image)
        
        doc.close()
        return images
    
    def process_page(self, page_number: int = 0) -> PDFPage:
        """
        Process a single page (extract text and images).
        
        Args:
            page_number: Zero-indexed page number
            
        Returns:
            Processed page data
        """
        text_blocks = self.extract_text_blocks(page_number)
        images = self.extract_images(page_number)
        
        # Get page dimensions
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[page_number]
            width = page.width
            height = page.height
        
        return PDFPage(
            page_number=page_number,
            text_blocks=text_blocks,
            images=images,
            width=width,
            height=height,
            has_text=len(text_blocks) > 0,
            has_images=len(images) > 0,
        )
    
    def process_all_pages(self) -> List[PDFPage]:
        """
        Process all pages in the PDF.
        
        Returns:
            List of processed pages
        """
        page_count = self.get_page_count()
        return [self.process_page(i) for i in range(page_count)]
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Extract PDF metadata.
        
        Returns:
            Dictionary with PDF metadata
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            return {
                "pages": len(pdf.pages),
                "metadata": pdf.metadata,
            }
