"""
Tests for matocr8d core functionality
"""

import pytest
import os
from PIL import Image
from unittest.mock import patch, MagicMock
import tempfile

from matocr8d import MatOCR8D, OCRError, ImageLoadError, UnsupportedFormatError


class TestMatOCR8D:
    """Test cases for MatOCR8D class"""
    
    def test_init_default(self):
        """Test default initialization"""
        ocr = MatOCR8D()
        assert ocr.language == 'eng'
    
    def test_init_with_language(self):
        """Test initialization with custom language"""
        ocr = MatOCR8D(language='spa')
        assert ocr.language == 'spa'
    
    def test_init_with_tesseract_cmd(self):
        """Test initialization with custom tesseract command"""
        with patch('pytesseract.pytesseract.tesseract_cmd'):
            ocr = MatOCR8D(tesseract_cmd='/custom/path')
            # The patch ensures we don't actually modify the global variable
    
    def test_supported_formats(self):
        """Test supported image formats"""
        ocr = MatOCR8D()
        expected_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        assert ocr.SUPPORTED_FORMATS == expected_formats
    
    def test_validate_image_path_not_exists(self):
        """Test validation of non-existent image path"""
        ocr = MatOCR8D()
        with pytest.raises(ImageLoadError, match="Image file not found"):
            ocr._validate_image_path("nonexistent.jpg")
    
    def test_validate_image_path_unsupported_format(self):
        """Test validation of unsupported image format"""
        ocr = MatOCR8D()
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with pytest.raises(UnsupportedFormatError, match="Unsupported image format"):
                ocr._validate_image_path(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_validate_image_path_success(self):
        """Test successful validation of image path"""
        ocr = MatOCR8D()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Should not raise any exception
            ocr._validate_image_path(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_load_image_with_path(self):
        """Test loading image from path"""
        ocr = MatOCR8D()
        
        # Create a simple test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            loaded_img = ocr._load_image(tmp_path)
            assert isinstance(loaded_img, Image.Image)
            assert loaded_img.size == (100, 100)
        finally:
            os.unlink(tmp_path)
    
    def test_load_image_with_pil_image(self):
        """Test loading PIL Image object"""
        ocr = MatOCR8D()
        img = Image.new('RGB', (50, 50), color='blue')
        
        loaded_img = ocr._load_image(img)
        assert loaded_img is img
    
    def test_load_image_invalid_input(self):
        """Test loading image with invalid input"""
        ocr = MatOCR8D()
        with pytest.raises(ImageLoadError, match="Input must be a file path or PIL Image"):
            ocr._load_image(123)
    
    @patch('pytesseract.image_to_string')
    def test_extract_text_success(self, mock_ocr):
        """Test successful text extraction"""
        mock_ocr.return_value = "Sample extracted text"
        
        ocr = MatOCR8D()
        img = Image.new('RGB', (100, 100), color='white')
        
        result = ocr.extract_text(img)
        assert result == "Sample extracted text"
        mock_ocr.assert_called_once()
    
    @patch('pytesseract.image_to_string')
    def test_extract_text_ocr_error(self, mock_ocr):
        """Test text extraction with OCR error"""
        mock_ocr.side_effect = Exception("OCR failed")
        
        ocr = MatOCR8D()
        img = Image.new('RGB', (100, 100), color='white')
        
        with pytest.raises(OCRError, match="OCR processing failed"):
            ocr.extract_text(img)
    
    @patch('pytesseract.image_to_data')
    @patch('pytesseract.image_to_string')
    def test_extract_text_with_data(self, mock_string, mock_data):
        """Test text extraction with metadata"""
        mock_string.return_value = "Sample text"
        mock_data.return_value = {
            'text': ['Sample', 'text'],
            'conf': [95, 85]
        }
        
        ocr = MatOCR8D()
        img = Image.new('RGB', (100, 100), color='white')
        
        result = ocr.extract_text_with_data(img)
        
        assert result['text'] == "Sample text"
        assert 'raw_data' in result
        assert 'confidence' in result
        assert 'word_count' in result
        assert result['word_count'] == 2
    
    def test_calculate_average_confidence(self):
        """Test confidence calculation"""
        ocr = MatOCR8D()
        data = {'conf': [90, 80, 0, 95]}  # 0 should be ignored
        avg_conf = ocr._calculate_average_confidence(data)
        assert avg_conf == (90 + 80 + 95) / 3
    
    def test_calculate_average_confidence_empty(self):
        """Test confidence calculation with empty data"""
        ocr = MatOCR8D()
        data = {'conf': []}
        avg_conf = ocr._calculate_average_confidence(data)
        assert avg_conf == 0.0
    
    @patch('pytesseract.image_to_data')
    def test_extract_text_blocks(self, mock_data):
        """Test text block extraction"""
        mock_data.return_value = {
            'text': ['Hello', '', 'World', ''],
            'conf': [95, 0, 85, 0],
            'left': [10, 0, 50, 0],
            'top': [10, 0, 10, 0],
            'width': [30, 0, 40, 0],
            'height': [10, 0, 10, 0]
        }
        
        ocr = MatOCR8D()
        img = Image.new('RGB', (100, 100), color='white')
        
        blocks = ocr.extract_text_blocks(img)
        
        assert len(blocks) == 2
        assert blocks[0]['text'] == 'Hello'
        assert blocks[0]['confidence'] == 95
        assert blocks[0]['bbox']['x'] == 10
        assert blocks[1]['text'] == 'World'
        assert blocks[1]['confidence'] == 85
    
    @patch('pytesseract.get_languages')
    def test_get_available_languages(self, mock_languages):
        """Test getting available languages"""
        mock_languages.return_value = ['eng', 'spa', 'fra']
        
        ocr = MatOCR8D()
        languages = ocr.get_available_languages()
        
        assert languages == ['eng', 'spa', 'fra']
    
    @patch('pytesseract.get_languages')
    def test_get_available_languages_error(self, mock_languages):
        """Test error when getting available languages"""
        mock_languages.side_effect = Exception("Failed to get languages")
        
        ocr = MatOCR8D()
        with pytest.raises(OCRError, match="Failed to get available languages"):
            ocr.get_available_languages()


class TestExceptions:
    """Test custom exceptions"""
    
    def test_ocr_error(self):
        """Test OCRError exception"""
        with pytest.raises(OCRError):
            raise OCRError("Test error")
    
    def test_image_load_error(self):
        """Test ImageLoadError exception"""
        with pytest.raises(ImageLoadError):
            raise ImageLoadError("Image load error")
    
    def test_unsupported_format_error(self):
        """Test UnsupportedFormatError exception"""
        with pytest.raises(UnsupportedFormatError):
            raise UnsupportedFormatError("Unsupported format")
