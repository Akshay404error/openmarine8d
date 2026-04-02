"""
Batch processing example for matocr8d library
"""

import os
import glob
from matocr8d import MatOCR8D, OCRError, ImageLoadError

def process_image_folder(folder_path, output_file="ocr_results.txt"):
    """
    Process all images in a folder and save results to a file
    
    Args:
        folder_path (str): Path to folder containing images
        output_file (str): Output file path for results
    """
    ocr = MatOCR8D()
    
    # Supported image extensions
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif', '*.webp']
    
    # Find all image files
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_files:
        print(f"No image files found in {folder_path}")
        return
    
    print(f"Found {len(image_files)} images to process")
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {os.path.basename(image_path)}")
        
        try:
            # Extract text with metadata
            result = ocr.extract_text_with_data(image_path)
            
            # Store result
            results.append({
                'filename': os.path.basename(image_path),
                'text': result['text'],
                'confidence': result['confidence'],
                'word_count': result['word_count']
            })
            
            print(f"  ✓ Extracted {result['word_count']} words (confidence: {result['confidence']:.2f})")
            
        except ImageLoadError as e:
            print(f"  ✗ Image loading error: {e}")
            results.append({
                'filename': os.path.basename(image_path),
                'error': str(e)
            })
        except OCRError as e:
            print(f"  ✗ OCR error: {e}")
            results.append({
                'filename': os.path.basename(image_path),
                'error': str(e)
            })
    
    # Save results to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("OCR Batch Processing Results\n")
        f.write("=" * 50 + "\n\n")
        
        for result in results:
            f.write(f"File: {result['filename']}\n")
            f.write("-" * 30 + "\n")
            
            if 'error' in result:
                f.write(f"Error: {result['error']}\n")
            else:
                f.write(f"Text: {result['text']}\n")
                f.write(f"Confidence: {result['confidence']:.2f}\n")
                f.write(f"Word Count: {result['word_count']}\n")
            
            f.write("\n" + "=" * 50 + "\n\n")
    
    print(f"\nResults saved to: {output_file}")
    print(f"Successfully processed {sum(1 for r in results if 'error' not in r)}/{len(results)} images")

def main():
    # Example usage
    folder_path = "sample_images"  # Replace with your folder path
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        print("Please create a folder named 'sample_images' and add some images")
        return
    
    process_image_folder(folder_path)

if __name__ == "__main__":
    main()
