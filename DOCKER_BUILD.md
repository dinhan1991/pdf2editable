# Docker Build and Test - V2 OCR

## Build Docker Image

```bash
cd pdf2editable
docker build -t pdf2editable:v2-ocr .
```

## Test Container

```bash
# Run container
docker run -d -p 8000:8000 --name pdf2editable-v2 pdf2editable:v2-ocr

# Check logs
docker logs pdf2editable-v2

# Test OCR inside container
docker exec pdf2editable-v2 tesseract --version
docker exec pdf2editable-v2 tesseract --list-langs

# Stop container
docker stop pdf2editable-v2
docker rm pdf2editable-v2
```

## Next Steps

1. Build Docker image
2. Test with user's scanned PDF
3. Verify Chinese character recognition
4. Measure performance
