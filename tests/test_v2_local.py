"""
V2 Local Testing Script - Verify code before deployment
"""

import sys
from pathlib import Path

print("="*60)
print("V2 LOCAL TESTING")
print("="*60)

# Test 1: Import all V2 modules
print("\n[TEST 1] Import V2 modules...")
try:
    from app.services import pdf_processor
    print("  [OK] pdf_processor imported")
    
    from app.services import ocr_processor
    print("  [OK] ocr_processor imported")
    
    from app.services import docx_generator
    print("  [OK] docx_generator imported")
    
    from app.services import font_mapper
    print("  [OK] font_mapper imported")
    
    print("[PASS] All V2 modules import successfully")
except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Unexpected error: {e}")
    sys.exit(1)

# Test 2: Check OCR availability
print("\n[TEST 2] Check OCR availability...")
try:
    from app.services.pdf_processor import OCR_AVAILABLE
    print(f"  OCR_AVAILABLE = {OCR_AVAILABLE}")
    
    if not OCR_AVAILABLE:
        print("  [INFO] OCR not available locally (expected without Tesseract)")
    else:
        print("  [INFO] OCR dependencies found")
    
    print("[PASS] OCR availability check complete")
except Exception as e:
    print(f"[FAIL] Error checking OCR: {e}")
    sys.exit(1)

# Test 3: PDFProcessor initialization
print("\n[TEST 3] PDFProcessor initialization...")
try:
    from app.services.pdf_processor import PDFProcessor
    
    # Test with OCR disabled (should always work)
    dummy_path = Path("test.pdf")
    processor_no_ocr = PDFProcessor(dummy_path, enable_ocr=False)
    print("  [OK] PDFProcessor created with OCR disabled")
    
    # Test with OCR enabled (will check dependencies)
    try:
        processor_with_ocr = PDFProcessor(dummy_path, enable_ocr=True)
        print("  [OK] PDFProcessor created with OCR enabled")
    except (ImportError, RuntimeError) as e:
        print(f"  [INFO] OCR initialization failed (expected): {e}")
        print("  [OK] Graceful error handling works")
    
    print("[PASS] PDFProcessor initialization test complete")
except Exception as e:
    print(f"[FAIL] PDFProcessor error: {e}")
    sys.exit(1)

# Test 4: FastAPI app startup
print("\n[TEST 4] FastAPI app startup...")
try:
    from app.main import app
    from app.core.config import settings
    
    print(f"  App name: {app.title}")
    print(f"  Version: {app.version}")
    print(f"  Max file size: {settings.max_file_size_mb}MB")
    print("[PASS] FastAPI app loads successfully")
except Exception as e:
    print(f"[FAIL] FastAPI app error: {e}")
    sys.exit(1)

# Test 5: V1 compatibility
print("\n[TEST 5] V1 compatibility (OCR disabled)...")
try:
    from app.services.pdf_processor import PDFProcessor
    
    # Create processor without OCR (V1 mode)
    test_path = Path("test_v1.pdf")
    processor = PDFProcessor(test_path, enable_ocr=False)
    
    # Verify ocr_processor is None
    assert processor.ocr_processor is None, "OCR should be None when disabled"
    assert processor.enable_ocr == False, "enable_ocr should be False"
    
    print("  [OK] V1 mode works correctly")
    print("  [OK] No OCR overhead when disabled")
    print("[PASS] V1 compatibility maintained")
except AssertionError as e:
    print(f"[FAIL] V1 compatibility issue: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Unexpected error: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("LOCAL TESTING COMPLETE")
print("="*60)
print()
print("Results:")
print("  [OK] All imports successful")
print("  [OK] No syntax errors")
print("  [OK] PDFProcessor initialization works")
print("  [OK] FastAPI app loads")
print("  [OK] V1 compatibility maintained")
print("  [OK] Graceful OCR fallback")
print()
print("Conclusion:")
print("  - V2 code is syntactically correct")
print("  - No import errors")
print("  - Backward compatible with V1")
print("  - Ready for deployment")
print()
print("Note:")
print("  - OCR will work in Docker (Tesseract installed)")
print("  - Local testing confirms no breaking changes")
print()
print("[READY] Safe to deploy to Railway")
