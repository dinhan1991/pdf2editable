# Tesseract OCR Setup Guide for Windows

## Quick Install (Recommended)

### Option 1: Using winget (Windows 10+)
```powershell
winget install UB-Mannheim.Tesseract
```

### Option 2: Manual Download
1. Download installer: https://github.com/UB-Mannheim/tesseract/releases/latest
2. Choose: `tesseract-ocr-w64-setup-x.x.x.exe` (64-bit)
3. Run installer
4. **Important**: Check "Additional language data" during installation
   - Select: Chinese (Simplified) - chi_sim
   - Select: Chinese (Traditional) - chi_tra
   - Select: Vietnamese - vie

### Option 3: Portable (No installation)
1. Download: `tesseract-ocr-w64-setup-x.x.x.exe`
2. Extract to: `C:\Tesseract`
3. Download language files manually

---

## Verify Installation

After installation, test:
```powershell
tesseract --version
```

Expected output:
```
tesseract 5.x.x
```

---

## Language Data Files

Location: `C:\Program Files\Tesseract-OCR\tessdata\`

Required files:
- `eng.traineddata` (default, included)
- `chi_sim.traineddata` (Chinese Simplified)
- `chi_tra.traineddata` (Chinese Traditional)
- `vie.traineddata` (Vietnamese)

If missing, download from:
https://github.com/tesseract-ocr/tessdata_fast

---

## Troubleshooting

### "tesseract is not recognized"
Add to PATH:
1. Open System Properties → Environment Variables
2. Edit "Path"
3. Add: `C:\Program Files\Tesseract-OCR`
4. Restart terminal

### Language data not found
```powershell
# Check tessdata directory
dir "C:\Program Files\Tesseract-OCR\tessdata\*.traineddata"
```

---

**Next**: Return to terminal and confirm Tesseract is installed
