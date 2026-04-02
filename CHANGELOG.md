# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of matocr8d OCR library
- Core OCR functionality with Tesseract integration
- Support for multiple image formats (JPEG, PNG, BMP, TIFF, WebP)
- Text extraction with confidence scores and metadata
- Text block extraction with bounding box coordinates
- Multi-language support
- Comprehensive error handling with custom exceptions
- Batch processing capabilities
- Full documentation and examples

### Features
- `MatOCR8D` main class for OCR operations
- `extract_text()` - Basic text extraction
- `extract_text_with_data()` - Text extraction with metadata
- `extract_text_blocks()` - Text blocks with coordinates
- `get_available_languages()` - List available OCR languages
- Support for both file paths and PIL Image objects
- Configurable Tesseract executable path

## [0.1.0] - 2024-03-30

### Added
- Initial public release
- Complete OCR library functionality
- PyPI publishing setup
- GitHub Actions CI/CD pipeline
- Comprehensive test suite
- Documentation and examples
