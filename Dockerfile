FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Tesseract OCR and language data
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-tra \
    tesseract-ocr-vie \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Verify Tesseract installation
RUN tesseract --version && tesseract --list-langs

# Copy requirements
COPY requirements.txt requirements-v2.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-v2.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MAX_FILE_SIZE_MB=150

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
