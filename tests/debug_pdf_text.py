"""
Debug script to check if PDF has extractable text or is image-based.
"""

import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path


def analyze_pdf(pdf_path: str):
    """Analyze PDF to detect if it has text layer or is image-only."""
    print("[DEBUG] PDF Analysis")
    print("=" * 60)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"[ERROR] PDF not found: {pdf_path}")
        return
    
    print(f"[INFO] File size: {pdf_file.stat().st_size / 1024 / 1024:.2f}MB")
    print("-" * 60)
    
    # Method 1: PyMuPDF text extraction
    print("\n[METHOD 1] PyMuPDF Text Extraction:")
    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        print(f"[INFO] Total pages: {page_count}")
        
        total_text_length = 0
        for page_num in range(min(3, page_count)):  # Check first 3 pages
            page = doc[page_num]
            text = page.get_text()
            text_length = len(text.strip())
            total_text_length += text_length
            
            print(f"[PAGE {page_num + 1}] Text length: {text_length} chars")
            if text_length > 0:
                preview = text.strip()[:100].replace('\n', ' ')
                print(f"         Preview: {preview}...")
        
        doc.close()
        
        if total_text_length == 0:
            print("[RESULT] NO TEXT FOUND - This is a SCANNED PDF (image-based)")
            print("[SOLUTION] Need OCR (V2 feature)")
        else:
            print(f"[RESULT] Text found ({total_text_length} chars in first 3 pages)")
            
    except Exception as e:
        print(f"[ERROR] PyMuPDF extraction failed: {e}")
    
    # Method 2: pdfplumber extraction
    print("\n[METHOD 2] pdfplumber Text Extraction:")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"[INFO] Total pages: {len(pdf.pages)}")
            
            for page_num in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    text_length = len(text.strip())
                    print(f"[PAGE {page_num + 1}] Text length: {text_length} chars")
                    if text_length > 0:
                        preview = text.strip()[:100].replace('\n', ' ')
                        print(f"         Preview: {preview}...")
                else:
                    print(f"[PAGE {page_num + 1}] No text found")
                    
    except Exception as e:
        print(f"[ERROR] pdfplumber extraction failed: {e}")
    
    # Method 3: Check for images
    print("\n[METHOD 3] Image Detection:")
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(3, len(doc))):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            print(f"[PAGE {page_num + 1}] Images found: {len(image_list)}")
            
            if len(image_list) > 0:
                for img_idx, img in enumerate(image_list[:3]):  # Show first 3 images
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    print(f"         Image {img_idx + 1}: {base_image['width']}x{base_image['height']} px")
        
        doc.close()
    except Exception as e:
        print(f"[ERROR] Image detection failed: {e}")
    
    print("=" * 60)
    print("\n[DIAGNOSIS]:")
    print("If 'NO TEXT FOUND' above:")
    print("  -> PDF is SCANNED (image-based, no text layer)")
    print("  -> Current V1 cannot extract text from scanned PDFs")
    print("  -> Need V2 with OCR (Tesseract/Google Vision)")
    print("\nIf text WAS found:")
    print("  -> PDF has text layer")
    print("  -> Bug in conversion code - investigate DOCXGenerator")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = r"C:\Users\dinhan\Downloads\20250917真空泵压缩机产品单页.pdf"
    
    analyze_pdf(pdf_path)
