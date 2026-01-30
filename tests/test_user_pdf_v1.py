"""
Test conversion with user's actual PDF file (V1 mode - no OCR locally)
"""

import httpx
import time
from pathlib import Path


def test_user_pdf_v1_mode():
    """Test with user's scanned Chinese PDF in V1 mode (images only)."""
    
    print("="*60)
    print("TESTING WITH USER'S SCANNED PDF")
    print("="*60)
    
    pdf_path = r"C:\Users\dinhan\Downloads\20250917真空泵压缩机产品单页.pdf"
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        print(f"[ERROR] PDF not found: {pdf_path}")
        return False
    
    file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"\n[INFO] PDF found")
    print(f"[INFO] File size: {file_size_mb:.2f}MB")
    print(f"[INFO] Mode: V1 (OCR disabled - no Tesseract locally)")
    print("-"*60)
    
    print("\n[STEP 1] Check server health...")
    try:
        response = httpx.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"[OK] Server healthy: {health['app']} v{health['version']}")
        else:
            print(f"[FAIL] Server returned {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Cannot connect to server: {e}")
        print("[ACTION] Start server with: uvicorn app.main:app --reload")
        return False
    
    print("\n[STEP 2] Upload and convert PDF (V1 mode)...")
    start = time.time()
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {
                'file': ('test.pdf', f, 'application/pdf')
            }
            data = {
                'preserve_fonts': 'true',
                'extract_images': 'true',
                # NOTE: enable_ocr=False by default (no Tesseract locally)
            }
            
            response = httpx.post(
                'http://localhost:8000/api/convert',
                files=files,
                data=data,
                timeout=120.0
            )
        
        elapsed = time.time() - start
        
        if response.status_code != 200:
            print(f"[FAIL] Conversion failed: {response.status_code}")
            print(f"[ERROR] {response.text}")
            return False
        
        result = response.json()
        print(f"[OK] Conversion completed in {elapsed:.2f}s")
        print(f"[INFO] Status: {result.get('status')}")
        print(f"[INFO] Pages: {result.get('pages_processed')}")
        print(f"[INFO] Server time: {result.get('processing_time_seconds')}s")
        
        file_id = result.get('file_id')
        
    except httpx.TimeoutException:
        print("[FAIL] Request timeout")
        return False
    except Exception as e:
        print(f"[FAIL] Conversion error: {e}")
        return False
    
    print("\n[STEP 3] Download DOCX...")
    try:
        download_response = httpx.get(
            f'http://localhost:8000/api/download/{file_id}',
            timeout=120.0
        )
        
        if download_response.status_code != 200:
            print(f"[FAIL] Download failed: {download_response.status_code}")
            return False
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"v1_test_{file_id}.docx"
        output_path.write_bytes(download_response.content)
        
        output_size_mb = len(download_response.content) / (1024 * 1024)
        print(f"[OK] Downloaded: {output_path}")
        print(f"[INFO] Size: {output_size_mb:.2f}MB")
        
    except Exception as e:
        print(f"[FAIL] Download error: {e}")
        return False
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    
    print("\nResults:")
    print(f"  - Conversion time: {elapsed:.2f}s")
    print(f"  - Pages processed: {result.get('pages_processed')}")
    print(f"  - Output file: {output_path}")
    
    print("\nV1 Mode Behavior (Expected):")
    print("  [NOTE] This is a scanned PDF (no text layer)")
    print("  [NOTE] V1 mode extracts images only")
    print("  [EXPECTED] DOCX will contain images (not editable text)")
    print("  [SOLUTION] Need V2 OCR (Railway deployment)")
    
    print("\nManual Verification:")
    print(f"  1. Open: {output_path}")
    print("  2. Check: Should see 11 pages of images")
    print("  3. Confirm: Images are clear (not text)")
    
    print("\nNext Steps:")
    print("  - V1 server works correctly")
    print("  - Ready for Railway deployment")
    print("  - Railway will have Tesseract OCR")
    print("  - V2 mode will extract editable text")
    
    return True


if __name__ == "__main__":
    import sys
    success = test_user_pdf_v1_mode()
    sys.exit(0 if success else 1)
