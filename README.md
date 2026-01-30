# PDF2Editable Word Tool

**AI-powered PDF to Word converter** với layout preservation, font mapping, và lossless image extraction.

## 🎯 Features

- ✅ **Layout Preservation**: Giữ nguyên columns, spacing, margins
- ✅ **Dung lượng**: Hỗ trợ file PDF tối đa 150MB.
- ✅ **Font Mapping**: Smart font substitution + custom font upload
- ✅ **Lossless Images**: Extract ảnh gốc với full DPI
- 🔄 **OCR Support** (V2): Chuyển đổi scanned PDFs
- 📊 **Complex Tables** (V2): Hỗ trợ merged cells
- ✏️ **Online Editor** (V3): Chỉnh sửa trước khi download

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip hoặc uv

### Installation

```bash
# Clone repository
git clone <repo-url>
cd pdf2editable

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Development Server

```bash
uvicorn app.main:app --reload
```

Server chạy tại: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## 📁 Project Structure

```
pdf2editable/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── endpoints/       # API routes
│   │   └── dependencies.py  # Shared dependencies
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Security utilities
│   ├── services/
│   │   ├── pdf_processor.py # PDF parsing & analysis
│   │   ├── docx_generator.py # DOCX creation
│   │   └── font_mapper.py   # Font substitution
│   └── models/
│       └── schemas.py       # Pydantic models
├── tests/
│   ├── test_pdf_processor.py
│   └── test_docx_generator.py
├── sample_pdfs/            # Test PDFs
├── output/                 # Generated DOCX files
├── docs/                   # Documentation
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_pdf_processor.py -v
```

## 📦 Docker Deployment

```bash
# Build image
docker build -t pdf2editable .

# Run container
docker run -p 8000:8000 pdf2editable
```

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.115+
- **PDF Processing**: pdfplumber, PyMuPDF
- **DOCX Generation**: python-docx
- **Runtime**: Python 3.12

## 📖 API Documentation

### Convert PDF to DOCX

```bash
POST /api/convert
Content-Type: multipart/form-data

{
  "file": <PDF file>,
  "preserve_fonts": true,
  "extract_images": true
}

Response:
{
  "file_id": "abc123",
  "status": "processing",
  "download_url": "/api/download/abc123"
}
```

### Download Converted File

```bash
GET /api/download/{file_id}

Response: application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

## 🗺️ Roadmap

- [x] **V1 (MVP)**: Text-based PDFs with basic layout
- [ ] **V2**: OCR + Advanced table detection
- [ ] **V3**: Online WYSIWYG editor

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md)

## 📧 Contact

Issues: [GitHub Issues](https://github.com/username/pdf2editable/issues)
