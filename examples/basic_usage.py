"""
Basic usage example for matocr8d library
"""

import os
from matocr8d import MatOCR8D, OCRError, ImageLoadError

def main():
    # Initialize OCR engine
    ocr = MatOCR8D()
    
    # Example image path (replace with your image)
    image_path = "sample_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"Sample image not found: {image_path}")
        print("Please place a sample image named 'sample_image.jpg' in the current directory")
        return
    
    try:
        # Basic text extraction
        print("=== Basic Text Extraction ===")
        text = ocr.extract_text(image_path)
        print(f"Extracted text:\n{text}\n")
        
        # Text extraction with metadata
        print("=== Text with Metadata ===")
        result = ocr.extract_text_with_data(image_path)
        print(f"Text: {result['text']}")
        print(f"Average confidence: {result['confidence']:.2f}")
        print(f"Word count: {result['word_count']}\n")
        
        # Text blocks with coordinates
        print("=== Text Blocks with Coordinates ===")
        blocks = ocr.extract_text_blocks(image_path)
        for i, block in enumerate(blocks[:5]):  # Show first 5 blocks
            bbox = block['bbox']
            print(f"Block {i+1}: '{block['text']}'")
            print(f"  Position: ({bbox['x']}, {bbox['y']})")
            print(f"  Size: {bbox['width']}x{bbox['height']}")
            print(f"  Confidence: {block['confidence']}\n")
        
        # Available languages
        print("=== Available Languages ===")
        languages = ocr.get_available_languages()
        print(f"Available languages: {', '.join(languages[:10])}...")  # Show first 10
        
    except ImageLoadError as e:
        print(f"Image loading error: {e}")
    except OCRError as e:
        print(f"OCR processing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
