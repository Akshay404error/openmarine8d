"""
matocr8d - A simple OCR library for Python

This library provides easy-to-use OCR functionality with support for
multiple image formats and text extraction capabilities.
"""

from .core import MatOCR8D
from .exceptions import OCRError, ImageLoadError

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "MatOCR8D",
    "OCRError", 
    "ImageLoadError"
]
