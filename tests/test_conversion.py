"""
Test PDF to DOCX conversion with actual file.
"""

import httpx
import time
from pathlib import Path


def test_pdf_conversion(pdf_path: str):
    """Test full conversion workflow."""
    print("[TEST] PDF to DOCX Conversion")
    print("=" * 60)
    
    # Check if file exists
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"[FAIL] PDF file not found: {pdf_path}")
        return False
    
    file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"[INFO] File size: {file_size_mb:.2f}MB")
    print("-" * 60)
    
    # Test 1: Upload and convert
    print("[STEP 1] Uploading PDF to server...")
    start_time = time.time()
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (pdf_file.name, f, 'application/pdf')}
            data = {
                'preserve_fonts': True,
                'extract_images': True,
            }
            
            response = httpx.post(
                'http://localhost:8000/api/convert',
                files=files,
                data=data,
                timeout=60.0  # 60 second timeout
            )
        
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"[FAIL] Server returned status {response.status_code}")
            print(f"[ERROR] {response.text}")
            return False
        
        result = response.json()
        print(f"[PASS] Conversion completed in {elapsed:.2f}s")
        print(f"[INFO] Status: {result.get('status')}")
        print(f"[INFO] Pages processed: {result.get('pages_processed')}")
        print(f"[INFO] Server processing time: {result.get('processing_time_seconds')}s")
        print(f"[INFO] File ID: {result.get('file_id')}")
        
        file_id = result.get('file_id')
        
    except httpx.TimeoutException:
        print(f"[FAIL] Request timeout (>60s)")
        return False
    except Exception as e:
        print(f"[FAIL] Upload error: {e}")
        return False
    
    print("-" * 60)
    
    # Test 2: Download converted file
    print("[STEP 2] Downloading converted DOCX...")
    try:
        download_response = httpx.get(
            f'http://localhost:8000/api/download/{file_id}',
            timeout=120.0  # Increased for large files
        )
        
        if download_response.status_code != 200:
            print(f"[FAIL] Download failed with status {download_response.status_code}")
            return False
        
        # Save to output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / f"converted_{file_id}.docx"
        output_path.write_bytes(download_response.content)
        
        output_size_mb = len(download_response.content) / (1024 * 1024)
        print(f"[PASS] DOCX downloaded successfully")
        print(f"[INFO] Output file: {output_path}")
        print(f"[INFO] Output size: {output_size_mb:.2f}MB")
        
    except Exception as e:
        print(f"[FAIL] Download error: {e}")
        return False
    
    print("=" * 60)
    print("[RESULT] Conversion test completed successfully!")
    print()
    print("Performance Summary:")
    print(f"  - Total time: {elapsed:.2f}s")
    print(f"  - Pages: {result.get('pages_processed')}")
    if result.get('pages_processed'):
        time_per_page = elapsed / result.get('pages_processed')
        print(f"  - Time per page: {time_per_page:.2f}s")
        
        # PRD requirement check
        if result.get('pages_processed') == 10:
            target = 15.0
            if elapsed < target:
                print(f"  - PRD Check (10 pages < 15s): [PASS] {elapsed:.2f}s < {target}s")
            else:
                print(f"  - PRD Check (10 pages < 15s): [FAIL] {elapsed:.2f}s > {target}s")
    
    print()
    print("Manual Verification Needed:")
    print(f"  1. Open {output_path} in Microsoft Word")
    print("  2. Check if content is readable")
    print("  3. Verify layout preservation")
    print("  4. Check font rendering (Chinese characters)")
    print("  5. Test editability")
    
    return True


if __name__ == "__main__":
    import sys
    
    # Get PDF path from command line or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = r"C:\Users\dinhan\Downloads\20250917真空泵压缩机产品单页.pdf"
    
    success = test_pdf_conversion(pdf_path)
    sys.exit(0 if success else 1)
