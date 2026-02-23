#!/usr/bin/env python3
"""
Batch process Gemini-generated images:
1. Remove Gemini logo/watermark from bottom right
2. Use OCR to identify menu items
3. Rename files based on identified items
"""

import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json

# Try importing OCR libraries
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not available. Install with: pip install pytesseract")
    print("Also need Tesseract OCR: brew install tesseract (Mac) or download from GitHub")

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False


class ImageProcessor:
    """Process Gemini images: remove watermark and identify content"""
    
    def __init__(self, input_dir, output_dir="images/processed", crop_percent=0.15):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.crop_percent = crop_percent  # Percentage to crop from bottom-right
        
        # Load menu items for matching
        self.menu_items = self._load_menu_items()
        
        # Initialize OCR
        self.ocr_engine = None
        self._init_ocr()
    
    def _load_menu_items(self):
        """Load menu items from JSON"""
        json_path = Path("menu_items.json")
        if json_path.exists():
            with open(json_path, 'r') as f:
                data = json.load(f)
                items = {}
                for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
                    for item in data.get(category, []):
                        items[item['id']] = {
                            'title': item['title'],
                            'keywords': self._extract_keywords(item['title'], item.get('ingredients', []))
                        }
                return items
        return {}
    
    def _extract_keywords(self, title, ingredients):
        """Extract searchable keywords from title and ingredients"""
        keywords = []
        # Add title words
        keywords.extend(title.lower().split())
        # Add key ingredient words
        for ing in ingredients:
            keywords.extend(ing.lower().split())
        return keywords
    
    def _init_ocr(self):
        """Initialize OCR engine"""
        if OCR_AVAILABLE:
            try:
                # Test if tesseract is available
                pytesseract.get_tesseract_version()
                self.ocr_engine = 'tesseract'
                print("✓ Tesseract OCR initialized")
            except Exception as e:
                print(f"⚠ Tesseract not found: {e}")
                self.ocr_engine = None
        elif PADDLE_AVAILABLE:
            try:
                self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
                print("✓ PaddleOCR initialized")
            except Exception as e:
                print(f"⚠ PaddleOCR error: {e}")
                self.ocr_engine = None
        else:
            print("⚠ No OCR engine available")
    
    def remove_watermark(self, image_path):
        """
        Remove Gemini watermark from bottom-right corner
        Strategy: Crop bottom-right corner and replace with blurred/inpainted area
        """
        img = Image.open(image_path)
        width, height = img.size
        
        # Calculate crop area (bottom-right corner)
        crop_width = int(width * self.crop_percent)
        crop_height = int(height * self.crop_percent)
        
        # Create a copy for processing
        processed = img.copy()
        
        # Method 1: Simple crop (remove bottom-right corner)
        # Crop the image to remove bottom-right
        cropped = img.crop((0, 0, width - crop_width, height - crop_height))
        
        # Resize back to original size (stretches slightly, but better than watermark)
        # Or better: extend with blurred edge
        result = Image.new('RGB', (width, height), (255, 255, 255))
        result.paste(cropped, (0, 0))
        
        # Blur the bottom-right area to blend
        if crop_width > 0 and crop_height > 0:
            # Get area to blur (extend beyond crop)
            blur_area = img.crop((width - crop_width * 2, height - crop_height * 2, width, height))
            blurred = blur_area.filter(ImageFilter.GaussianBlur(radius=10))
            result.paste(blurred, (width - crop_width * 2, height - crop_height * 2))
        
        return result
    
    def extract_text_ocr(self, image_path):
        """Extract text from image using OCR"""
        if not self.ocr_engine:
            return ""
        
        try:
            img = Image.open(image_path)
            
            if self.ocr_engine == 'tesseract':
                # Use Tesseract
                text = pytesseract.image_to_string(img, lang='eng')
                return text.lower()
            elif isinstance(self.ocr_engine, PaddleOCR):
                # Use PaddleOCR
                result = self.ocr_engine.ocr(str(image_path), cls=True)
                if result and result[0]:
                    text = ' '.join([line[1][0] for line in result[0]])
                    return text.lower()
        except Exception as e:
            print(f"  OCR error: {e}")
        
        return ""
    
    def identify_menu_item(self, text, filename):
        """Try to identify which menu item this image represents"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        best_match = None
        best_score = 0
        
        for item_id, item_data in self.menu_items.items():
            title = item_data['title'].lower()
            keywords = item_data['keywords']
            
            score = 0
            # Check if title appears in text
            if title in text_lower or any(word in text_lower for word in title.split()):
                score += 10
            
            # Check keyword matches
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            # Check filename
            if item_id.replace('-', ' ') in filename_lower or title in filename_lower:
                score += 5
            
            if score > best_score:
                best_score = score
                best_match = item_id
        
        return best_match, best_score
    
    def process_image(self, image_path):
        """Process a single image: remove watermark and identify"""
        print(f"\nProcessing: {image_path.name}")
        
        # Remove watermark
        processed_img = self.remove_watermark(image_path)
        
        # Save processed image temporarily for OCR
        temp_path = self.output_dir / f"temp_{image_path.name}"
        processed_img.save(temp_path)
        
        # Extract text with OCR
        print("  Extracting text with OCR...")
        text = self.extract_text_ocr(temp_path)
        
        if text:
            print(f"  Found text: {text[:100]}...")
        
        # Identify menu item
        item_id, score = self.identify_menu_item(text, image_path.name)
        
        if item_id and score > 3:
            new_filename = f"{item_id}.png"
            print(f"  ✓ Identified as: {self.menu_items[item_id]['title']} (score: {score})")
        else:
            # Keep original name but clean it up
            new_filename = image_path.stem.replace("Gemini_Generated_Image_", "").replace(" ", "-") + ".png"
            print(f"  ⚠ Could not identify (score: {score}), using: {new_filename}")
        
        # Save final image
        final_path = self.output_dir / new_filename
        processed_img.save(final_path, quality=95)
        print(f"  ✓ Saved: {final_path.name}")
        
        # Clean up temp file
        temp_path.unlink()
        
        return {
            'original': image_path.name,
            'new': new_filename,
            'identified': item_id,
            'score': score,
            'text': text[:200] if text else ""
        }
    
    def process_all(self):
        """Process all images in input directory"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_files = [f for f in self.input_dir.iterdir() 
                      if f.suffix.lower() in image_extensions and f.is_file()]
        
        if not image_files:
            print(f"No images found in {self.input_dir}")
            return
        
        print(f"Found {len(image_files)} images to process")
        print(f"Output directory: {self.output_dir}")
        
        results = []
        for image_file in sorted(image_files):
            try:
                result = self.process_image(image_file)
                results.append(result)
            except Exception as e:
                print(f"  ✗ Error processing {image_file.name}: {e}")
        
        # Save results summary
        summary_path = self.output_dir / "processing_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"Processing Complete!")
        print(f"{'='*60}")
        print(f"Processed: {len(results)} images")
        print(f"Output: {self.output_dir}")
        print(f"Summary: {summary_path}")
        
        # Show identification stats
        identified = [r for r in results if r['identified']]
        print(f"\nIdentified: {len(identified)}/{len(results)} images")
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Process Gemini images: remove watermark and identify")
    parser.add_argument("--input", default="Brand Assets/100k Shakes gemini renders",
                       help="Input directory with Gemini images")
    parser.add_argument("--output", default="images/processed",
                       help="Output directory for processed images")
    parser.add_argument("--crop", type=float, default=0.15,
                       help="Percentage to crop from bottom-right (0.15 = 15%%)")
    
    args = parser.parse_args()
    
    processor = ImageProcessor(args.input, args.output, args.crop)
    processor.process_all()


if __name__ == "__main__":
    main()


