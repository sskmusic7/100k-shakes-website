#!/usr/bin/env python3
"""
Identify and rename shake images using OCR and vision analysis
Matches images to menu items from menu_items.json
"""

import os
import json
import re
from pathlib import Path
from PIL import Image
import hashlib

# Try importing OCR
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠ pytesseract not available. Install with: pip install pytesseract")

# Try importing vision API (Google Gemini Vision)
try:
    import google.generativeai as genai
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("⚠ Google Generative AI not available. Install with: pip install google-generativeai")


class ImageIdentifier:
    """Identify menu items in images using OCR and vision"""
    
    def __init__(self, menu_json_path="menu_items.json"):
        self.menu_items = self._load_menu_items(menu_json_path)
        self.vision_model = None
        self._init_vision()
    
    def _load_menu_items(self, json_path):
        """Load menu items and create searchable index"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        items = {}
        for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
            for item in data.get(category, []):
                items[item['id']] = {
                    'title': item['title'],
                    'category': category,
                    'keywords': self._extract_keywords(item),
                    'description': item.get('prompt', ''),
                    'ingredients': item.get('ingredients', [])
                }
        return items
    
    def _extract_keywords(self, item):
        """Extract all searchable keywords from menu item"""
        keywords = []
        # Title words
        keywords.extend(item['title'].lower().split())
        # Ingredient words
        for ing in item.get('ingredients', []):
            keywords.extend(ing.lower().split())
        # Prompt keywords
        prompt = item.get('prompt', '').lower()
        # Extract key flavor/color words
        color_words = ['pink', 'brown', 'chocolate', 'strawberry', 'vanilla', 'caramel', 'golden', 'dark', 'white', 'cream']
        for word in color_words:
            if word in prompt:
                keywords.append(word)
        # Extract key ingredient mentions
        if 'oreo' in prompt:
            keywords.append('oreo')
        if 'milo' in prompt:
            keywords.append('milo')
        if 'jager' in prompt or 'jäger' in prompt:
            keywords.append('jager')
        if 'amarula' in prompt:
            keywords.append('amarula')
        if 'baileys' in prompt:
            keywords.append('baileys')
        if 'espresso' in prompt or 'coffee' in prompt:
            keywords.append('espresso')
        if 'cone' in prompt:
            keywords.append('cone')
        if 'vegan' in prompt.lower():
            keywords.append('vegan')
        
        return list(set(keywords))  # Remove duplicates
    
    def _init_vision(self):
        """Initialize Google Vision API if available"""
        if VISION_AVAILABLE:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
                    print("✓ Vision API initialized")
                except Exception as e:
                    print(f"⚠ Vision API error: {e}")
            else:
                print("⚠ GOOGLE_API_KEY not set. Vision analysis disabled.")
    
    def extract_text_ocr(self, image_path):
        """Extract text from image using OCR"""
        if not OCR_AVAILABLE:
            return ""
        
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='eng')
            return text.lower()
        except Exception as e:
            return ""
    
    def analyze_with_vision(self, image_path):
        """Analyze image using Google Vision API"""
        if not self.vision_model:
            return None
        
        try:
            img = Image.open(image_path)
            prompt = """Analyze this milkshake or ice cream image and identify:
1. The flavor/type (e.g., Oreo, Strawberry, Chocolate, Vanilla, Caramel, Milo, Jägermeister, Amarula, Baileys, Espresso)
2. Key visual features (colors, toppings, ingredients visible)
3. Whether it's a milkshake in a cup or ice cream cone
4. Whether it appears to be vegan (plant-based indicators)

Respond with a brief description focusing on identifying the specific menu item."""
            
            response = self.vision_model.generate_content([prompt, img])
            return response.text.lower()
        except Exception as e:
            print(f"  Vision API error: {e}")
            return None
    
    def identify_menu_item(self, image_path, use_vision=True):
        """Identify which menu item this image represents"""
        print(f"\nAnalyzing: {image_path.name}")
        
        # Method 1: OCR
        ocr_text = self.extract_text_ocr(image_path)
        if ocr_text:
            print(f"  OCR text: {ocr_text[:100]}...")
        
        # Method 2: Vision API
        vision_text = None
        if use_vision and self.vision_model:
            print("  Using Vision API...")
            vision_text = self.analyze_with_vision(image_path)
            if vision_text:
                print(f"  Vision analysis: {vision_text[:150]}...")
        
        # Combine all text for matching
        all_text = f"{ocr_text} {vision_text or ''}".lower()
        
        # Score each menu item
        best_match = None
        best_score = 0
        scores = {}
        
        for item_id, item_data in self.menu_items.items():
            score = 0
            title = item_data['title'].lower()
            keywords = item_data['keywords']
            
            # Title match (strong signal)
            if title in all_text:
                score += 20
            # Partial title match
            for word in title.split():
                if word in all_text:
                    score += 5
            
            # Keyword matches
            for keyword in keywords:
                if keyword in all_text:
                    score += 2
            
            # Category-specific checks
            if item_data['category'] == 'icecream' and ('cone' in all_text or 'ice cream' in all_text):
                score += 10
            if item_data['category'] == 'shotshake' and ('21+' in all_text or 'alcohol' in all_text):
                score += 10
            if item_data['category'] == 'vegan' and ('vegan' in all_text or 'plant' in all_text):
                score += 10
            
            # Specific ingredient matches
            if 'oreo' in all_text and 'oreo' in keywords:
                score += 15
            if 'strawberry' in all_text and 'strawberry' in keywords:
                score += 15
            if 'milo' in all_text and 'milo' in keywords:
                score += 15
            if 'jager' in all_text or 'jäger' in all_text:
                score += 15
            if 'amarula' in all_text:
                score += 15
            if 'baileys' in all_text:
                score += 15
            if 'espresso' in all_text or 'coffee' in all_text:
                score += 15
            
            scores[item_id] = score
            
            if score > best_score:
                best_score = score
                best_match = item_id
        
        # Show top 3 matches
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  Top matches:")
        for item_id, score in sorted_scores:
            print(f"    - {self.menu_items[item_id]['title']}: {score} points")
        
        if best_match and best_score >= 5:
            return best_match, best_score
        else:
            return None, best_score
    
    def process_directory(self, directory, output_dir=None, use_vision=True):
        """Process all images in a directory"""
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Directory not found: {directory}")
            return
        
        # Find all image files
        image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.heic'}
        image_files = [f for f in dir_path.rglob('*') 
                       if f.suffix.lower() in image_extensions and f.is_file()]
        
        if not image_files:
            print(f"No images found in {directory}")
            return
        
        print(f"\n{'='*60}")
        print(f"Processing {len(image_files)} images in {directory}")
        print(f"{'='*60}")
        
        results = []
        renamed_count = 0
        
        for img_file in sorted(image_files):
            try:
                item_id, score = self.identify_menu_item(img_file, use_vision)
                
                if item_id and score >= 5:
                    # Create new filename
                    item_data = self.menu_items[item_id]
                    new_filename = f"{item_id}{img_file.suffix}"
                    
                    # Determine output path
                    if output_dir:
                        output_path = Path(output_dir) / new_filename
                    else:
                        output_path = img_file.parent / new_filename
                    
                    # Handle duplicates
                    counter = 1
                    original_output = output_path
                    while output_path.exists():
                        output_path = original_output.parent / f"{item_id}_{counter}{img_file.suffix}"
                        counter += 1
                    
                    # Rename file
                    img_file.rename(output_path)
                    print(f"  ✓ Renamed to: {output_path.name}")
                    renamed_count += 1
                    
                    results.append({
                        'original': img_file.name,
                        'new': output_path.name,
                        'item_id': item_id,
                        'title': item_data['title'],
                        'score': score
                    })
                else:
                    print(f"  ⚠ Could not identify (score: {score})")
                    results.append({
                        'original': img_file.name,
                        'new': None,
                        'item_id': None,
                        'title': None,
                        'score': score
                    })
            except Exception as e:
                print(f"  ✗ Error processing {img_file.name}: {e}")
                results.append({
                    'original': img_file.name,
                    'error': str(e)
                })
        
        print(f"\n{'='*60}")
        print(f"Complete: {renamed_count}/{len(image_files)} images renamed")
        print(f"{'='*60}")
        
        # Save results
        results_file = Path(directory) / "identification_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {results_file}")
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Identify and rename shake images")
    parser.add_argument("--input", default="GUIDANCE DOCS/100k Shakes Renders",
                       help="Input directory")
    parser.add_argument("--output", help="Output directory (default: same as input)")
    parser.add_argument("--no-vision", action="store_true",
                       help="Disable Vision API (use only OCR)")
    parser.add_argument("--menu-json", default="menu_items.json",
                       help="Path to menu items JSON")
    
    args = parser.parse_args()
    
    identifier = ImageIdentifier(args.menu_json)
    
    # Process subdirectories
    base_dir = Path(args.input)
    
    # Process each category folder
    folders_to_process = [
        base_dir / "Z Image Renders",
        base_dir / "Vegan Delights",
        base_dir / "Icecream cones",
        base_dir / "100k Shakes gemini renders"
    ]
    
    for folder in folders_to_process:
        if folder.exists():
            output = args.output or str(folder)
            identifier.process_directory(str(folder), output, use_vision=not args.no_vision)


if __name__ == "__main__":
    main()
