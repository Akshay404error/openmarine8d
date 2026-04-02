# Tesseract OCR Installation Guide

## Windows Installation

### Method 1: Download Installer (Recommended)

1. **Download Tesseract** from: https://github.com/UB-Mannheim/tesseract/wiki
2. Click on **"tesseract-ocr-w64-setup-5.3.3-20231118.exe"** (or latest version)
3. Run the installer
4. **Important**: During installation, check the box to **"Add Tesseract to your PATH"**
5. Complete installation

### Method 2: Using Chocolatey

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Tesseract
choco install tesseract
```

### Method 3: Using pip (Python wrapper)

```bash
pip install pytesseract
```

## Verify Installation

### Test Tesseract in Command Prompt

```cmd
tesseract --version
```

You should see something like:
```
tesseract 5.3.3
 leptonica-1.84.1
  libgif 5.2.1 : libjpeg 9e : libpng 1.6.40 : libtiff 4.6.0 : zlib 1.2.13 : libwebp 1.3.2 : libopenjp2 2.5.0
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found libarchive 3.7.2
 Found libcurl 8.4.0
```

### Test Python Integration

```python
import pytesseract
print(pytesseract.get_tesseract_version())
```

## If Tesseract is Not in PATH

If you didn't add Tesseract to PATH during installation, you can:

### Option 1: Add to PATH Manually

1. Find Tesseract installation path (usually: `C:\Program Files\Tesseract-OCR`)
2. Add to Windows PATH:
   - Press `Win + R`, type `sysdm.cpl`
   - Go to "Advanced" → "Environment Variables"
   - Edit "Path" variable
   - Add `C:\Program Files\Tesseract-OCR`

### Option 2: Specify Path in Code

```python
from matocr8d import MatOCR8D

# Specify Tesseract path
ocr = MatOCR8D(tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe')

# Test
text = ocr.extract_text('test_image.png')
print(text)
```

## Install Language Packs (Optional)

If you need languages other than English:

1. Download language data from: https://github.com/tesseract-ocr/tessdata
2. Copy `.traineddata` files to: `C:\Program Files\Tesseract-OCR\tessdata`
3. Use language code when initializing:
   ```python
   ocr = MatOCR8D(language='spa')  # Spanish
   ```

## Quick Test After Installation

Run your sample script again:
```bash
python sample.py
```

It should now work without the Tesseract error!
