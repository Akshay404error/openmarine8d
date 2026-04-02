# matocr8d

A simple and easy-to-use OCR (Optical Character Recognition) library for Python that leverages Tesseract OCR engine for text extraction from images.

## Features

- Extract text from various image formats (JPEG, PNG, BMP, TIFF, WebP)
- Support for multiple languages
- Get text with confidence scores and metadata
- Extract text blocks with bounding box coordinates
- Simple and intuitive API
- Comprehensive error handling

## Installation

### Prerequisites

1. Install Tesseract OCR on your system:
   
   **Windows:**
   ```bash
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   # Make sure to add Tesseract to your PATH
   ```
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

2. Install additional language packs if needed:
   ```bash
   # Ubuntu/Debian
   sudo apt install tesseract-ocr-[lang_code]
   
   # Example for Spanish
   sudo apt install tesseract-ocr-spa
   ```

### Install the library

```bash
pip install matocr8d
```

Or install from source:
```bash
git clone https://github.com/Akshay404error/OCR-library-python.git
cd OCR-library-python
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from matocr8d import MatOCR8D

# Initialize OCR engine
ocr = MatOCR8D()

# Extract text from image file
text = ocr.extract_text("path/to/image.jpg")
print(text)

# Extract text with metadata
result = ocr.extract_text_with_data("path/to/image.jpg")
print(f"Text: {result['text']}")
print(f"Confidence: {result['confidence']}")
print(f"Word count: {result['word_count']}")

# Extract text blocks with coordinates
blocks = ocr.extract_text_blocks("path/to/image.jpg")
for block in blocks:
    print(f"Text: '{block['text']}' at {block['bbox']}")
```

## Advanced Usage

### Using Different Languages

```python
# Initialize with Spanish language
ocr = MatOCR8D(language='spa')

# Get available languages
languages = ocr.get_available_languages()
print(f"Available languages: {languages}")
```

### Custom Tesseract Path

```python
# Specify custom Tesseract executable path
ocr = MatOCR8D(tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract.exe')
```

### Using PIL Image Objects

```python
from PIL import Image
from matocr8d import MatOCR8D

# Load image with PIL
image = Image.open("path/to/image.jpg")

# Extract text from PIL Image object
ocr = MatOCR8D()
text = ocr.extract_text(image)
print(text)
```

## API Reference

### MatOCR8D Class

#### Constructor

```python
MatOCR8D(language='eng', tesseract_cmd=None)
```

- `language` (str): Language code for OCR (default: 'eng')
- `tesseract_cmd` (str, optional): Path to Tesseract executable

#### Methods

##### `extract_text(image_input)`

Extract plain text from an image.

**Parameters:**
- `image_input` (str or PIL.Image): Path to image file or PIL Image object

**Returns:**
- `str`: Extracted text

##### `extract_text_with_data(image_input)`

Extract text with additional metadata.

**Parameters:**
- `image_input` (str or PIL.Image): Path to image file or PIL Image object

**Returns:**
- `dict`: Dictionary containing:
  - `text`: Extracted text
  - `raw_data`: Raw OCR data
  - `confidence`: Average confidence score
  - `word_count`: Number of words detected

##### `extract_text_blocks(image_input)`

Extract text blocks with bounding box coordinates.

**Parameters:**
- `image_input` (str or PIL.Image): Path to image file or PIL Image object

**Returns:**
- `list`: List of dictionaries containing:
  - `text`: Text block content
  - `confidence`: Confidence score
  - `bbox`: Bounding box coordinates (x, y, width, height)

##### `get_available_languages()`

Get list of available OCR languages.

**Returns:**
- `list`: Available language codes

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Error Handling

The library provides custom exceptions for better error handling:

- `OCRError`: Base exception for OCR-related errors
- `ImageLoadError`: Raised when an image cannot be loaded
- `UnsupportedFormatError`: Raised when an unsupported image format is provided

```python
from matocr8d import MatOCR8D, OCRError, ImageLoadError

ocr = MatOCR8D()

try:
    text = ocr.extract_text("nonexistent.jpg")
except ImageLoadError as e:
    print(f"Image error: {e}")
except OCRError as e:
    print(f"OCR error: {e}")
```

## Examples

Check the `examples/` directory for more usage examples:

- Basic text extraction
- Batch processing
- Text detection with confidence filtering
- Multi-language OCR

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for the OCR engine
- [Pillow](https://pillow.readthedocs.io/) for image processing
- [pytesseract](https://pypi.org/project/pytesseract/) for Python Tesseract wrapper
