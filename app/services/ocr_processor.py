"""OCR Processor for extracting text from images using Tesseract."""

from typing import List, Optional
from pathlib import Path
from io import BytesIO

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from app.models.schemas import PDFTextBlock


class OCRProcessor:
    """Extract text from images using Tesseract OCR."""
    
    def __init__(self, languages: Optional[List[str]] = None):
        """
        Initialize OCR processor.
        
        Args:
            languages: List of language codes (e.g., ['chi_sim', 'eng'])
                      Default: ['chi_sim', 'eng'] for Chinese + English
        """
        if not TESSERACT_AVAILABLE:
            raise ImportError(
                "pytesseract not installed. Install with: pip install pytesseract"
            )
        
        self.languages = languages or ['chi_sim', 'eng']
        self.lang_string = '+'.join(self.languages)
        
        # Verify Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(
                f"Tesseract not found. Please install Tesseract OCR. Error: {e}"
            )
    
    def extract_text_from_image(
        self, 
        image_data: bytes,
        page_number: int = 0
    ) -> List[PDFTextBlock]:
        """
        Extract text from image using OCR.
        
        Args:
            image_data: Image bytes
            page_number: Page number for metadata
            
        Returns:
            List of text blocks extracted from image
        """
        try:
            # Load image
            image = Image.open(BytesIO(image_data))
            
            # Preprocess image for better OCR
            image = self._preprocess_image(image)
            
            # Perform OCR
            text = pytesseract.image_to_string(
                image,
                lang=self.lang_string,
                config='--psm 6'  # Assume uniform text block
            )
            
            if not text.strip():
                print(f"[OCR] No text extracted from page {page_number}")
                return []
            
            # Convert to text blocks format
            # For now, treat entire page as one block
            # TODO: Use image_to_data for word-level positioning
            text_block = PDFTextBlock(
                page_number=page_number,
                text=text.strip(),
                x0=0,
                y0=0,
                x1=image.width,
                y1=image.height,
                font_name="OCR-Result",
                font_size=12,
            )
            
            char_count = len(text.strip())
            print(f"[OCR] Extracted {char_count} characters from page {page_number}")
            
            return [text_block]
            
        except Exception as e:
            print(f"[OCR] Error extracting text from page {page_number}: {e}")
            return []
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy.
        
        Args:
            image: PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize if too large (OCR works better at certain DPI ~300)
        max_dimension = 4000
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def detect_language(self, image_data: bytes) -> str:
        """
        Auto-detect primary language in image.
        
        Args:
            image_data: Image bytes
            
        Returns:
            Detected language code
        """
        try:
            image = Image.open(BytesIO(image_data))
            image = self._preprocess_image(image)
            
            # Use OSD (Orientation and Script Detection)
            osd = pytesseract.image_to_osd(image)
            
            # Parse script from OSD output
            for line in osd.split('\n'):
                if line.startswith('Script:'):
                    script = line.split(':')[1].strip()
                    # Map script to language code
                    script_map = {
                        'Han': 'chi_sim',
                        'Latin': 'eng',
                        'Vietnamese': 'vie',
                    }
                    return script_map.get(script, 'eng')
            
            return 'eng'  # Default fallback
            
        except Exception as e:
            print(f"[OCR] Language detection failed: {e}")
            return 'eng'
