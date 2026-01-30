"""Simple test to verify server is running and responding."""

import httpx
import sys


def test_server():
    """Test server health and API docs."""
    print("[TEST] PDF2Editable V1 - Server Verification")
    print("=" * 50)
    
    # Test 1: Health endpoint
    try:
        response = httpx.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Server is healthy - {data.get('app')} v{data.get('version')}")
        else:
            print(f"[FAIL] Server returned status {response.status_code}")
            return False
    except httpx.ConnectError:
        print("[FAIL] Cannot connect to server")
        print(" " * 7 + "Start with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"[FAIL] Health check error: {e}")
        return False
    
    # Test 2: API docs
    try:
        response = httpx.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("[PASS] API docs accessible at http://localhost:8000/docs")
        else:
            print(f"[WARN] API docs returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] API docs error: {e}")
        return False
    
    print("=" * 50)
    print("[RESULT] All checks passed! Server is ready.")
    return True


if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
