# Quick Start Guide - PDF2Editable Word Tool

## 🚀 Setup trong 5 phút

### 1. Cài đặt Dependencies

```powershell
# Di chuyển vào thư mục project
cd c:\Users\dinhan\.gemini\antigravity\playground\glacial-tyson\pdf2editable

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment (Windows)
.\venv\Scripts\activate

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Cấu hình Environment

```powershell
# Copy file .env.example thành .env
copy .env.example .env

# File .env đã có default settings, không cần chỉnh gì thêm cho MVP
```

### 3. Chạy Development Server

```powershell
# Đảm bảo đang ở trong virtual environment
uvicorn app.main:app --reload
```

Server sẽ chạy tại: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## 🧪 Test API

### Option 1: Sử dụng Swagger UI (Recommended)

1. Mở browser vào `http://localhost:8000/docs`
2. Click vào endpoint `POST /api/convert`
3. Click "Try it out"
4. Upload file PDF (max 150MB)
5. Click "Execute"
6. Copy `file_id` từ response
7. Test download endpoint với file_id đó

### Option 2: Sử dụng cURL

```powershell
# Upload và convert PDF
curl -X POST "http://localhost:8000/api/convert" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@sample.pdf" `
  -F "preserve_fonts=true" `
  -F "extract_images=true"

# Response sẽ có file_id, ví dụ: "abc-123-def"

# Download converted DOCX
curl "http://localhost:8000/api/download/abc-123-def" --output converted.docx
```

### Option 3: Sử dụng Python

```python
import requests

# Convert PDF
with open("sample.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/convert",
        files={"file": f},
        data={
            "preserve_fonts": True,
            "extract_images": True,
        }
    )

result = response.json()
print(f"Status: {result['status']}")
print(f"Pages: {result['pages_processed']}")
print(f"Time: {result['processing_time_seconds']}s")

# Download DOCX
file_id = result['file_id']
docx_response = requests.get(f"http://localhost:8000/api/download/{file_id}")

with open(f"converted_{file_id}.docx", "wb") as f:
    f.write(docx_response.content)

print(f"✅ Downloaded: converted_{file_id}.docx")
```

---

## 📁 Project Structure

```
pdf2editable/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── api/
│   │   └── endpoints/
│   │       ├── health.py          # Health check
│   │       └── convert.py         # PDF→DOCX conversion
│   ├── core/
│   │   └── config.py              # Configuration settings
│   ├── services/
│   │   ├── pdf_processor.py       # PDF parsing (pdfplumber + PyMuPDF)
│   │   ├── docx_generator.py      # DOCX creation (python-docx)
│   │   └── font_mapper.py         # Font substitution logic
│   └── models/
│       └── schemas.py             # Pydantic models
├── output/                        # Generated DOCX files (auto-cleanup 1h)
├── uploads/                       # Temporary PDF uploads
└── sample_pdfs/                   # Test PDFs
```

---

## 🐞 Troubleshooting

### Lỗi: `ModuleNotFoundError: No module named 'app'`

**Giải pháp**: Đảm bảo đang chạy từ thư mục `pdf2editable/`

```powershell
cd c:\Users\dinhan\.gemini\antigravity\playground\glacial-tyson\pdf2editable
uvicorn app.main:app --reload
```

### Lỗi: `ImportError: cannot import name 'fitz'`

**Giải pháp**: Cài đặt lại PyMuPDF

```powershell
pip uninstall PyMuPDF
pip install PyMuPDF==1.24.14
```

### Lỗi: `FileNotFoundError: [Errno 2] No such file or directory: './output'`

**Giải pháp**: Directories sẽ tự động tạo khi server start. Nếu không, tạo thủ công:

```powershell
mkdir output, uploads, temp
```

### Server chạy nhưng không thể access /docs

**Giải pháp**: Check `.env` file, đảm bảo `DEBUG=true`

---

## ⚡ Performance Tips

### Speed up development reload

```powershell
# Sử dụng --reload-dir để chỉ watch app/ folder
uvicorn app.main:app --reload --reload-dir app
```

### Check processing speed

```python
# Test với file PDF mẫu
import time
start = time.time()

# ... upload file qua API ...

print(f"Time per page: {(time.time() - start) / pages:.2f}s")
# Target: <1.5s per page
```

---

## 🚢 Next Steps

1. ✅ Đã setup? → Test với PDF của bạn
2. ⚠️ Có lỗi? → Xem Troubleshooting section phía trên
3. 🎯 Muốn customize? → Xem `app/core/config.py` và `.env`
4. 🧪 Muốn test nâng cao? → Tạo file trong `sample_pdfs/` và viết unit tests

---

## 📝 Development Tips

### Watch logs

Server sẽ log ra console:
- File uploads
- Processing time
- Errors (nếu có)

### Hot reload

FastAPI tự động reload khi bạn save code, không cần restart server.

### Debug mode

Khi `DEBUG=true`, Swagger UI (`/docs`) sẽ available với full API documentation.

---

**Cần help?** Check README.md hoặc xem architecture document tại `docs/architecture/`
