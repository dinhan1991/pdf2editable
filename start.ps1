# Setup and Run - PDF2Editable Server
# Chạy script này để start server

Write-Host "🚀 PDF2Editable - Starting Server..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if venv exists
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Step 2: Activate venv and install dependencies
Write-Host "📥 Installing dependencies (this may take 1-2 minutes)..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".\venv\Scripts\pip.exe" install -r requirements.txt --quiet

Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Step 3: Setup .env if not exists
if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file" -ForegroundColor Green
}

# Step 4: Start server
Write-Host ""
Write-Host "🎉 Starting FastAPI server..." -ForegroundColor Cyan
Write-Host "📍 Server will run at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "📖 API docs at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop server" -ForegroundColor Gray
Write-Host ""

& ".\venv\Scripts\uvicorn.exe" app.main:app --reload
