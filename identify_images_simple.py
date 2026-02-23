#!/usr/bin/env python3
"""
Simplified image identifier using color analysis and basic OCR
Works without Vision API by analyzing image colors and patterns
"""

import os
import json
from pathlib import Path
from PIL import Image
import numpy as np

# Try OCR
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# Try Vision API
try:
    import google.generativeai as genai
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False


def get_dominant_colors(image_path, k=3):
    """Get dominant colors from image"""
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((150, 150))  # Resize for speed
        
        # Convert to numpy array
        arr = np.array(img)
        arr = arr.reshape(-1, 3)
        
        # Simple k-means (approximate)
        from collections import Counter
        # Sample pixels
        sample = arr[::10]  # Every 10th pixel
        colors = [tuple(c) for c in sample]
        color_counts = Counter(colors)
        top_colors = [c[0] for c in color_counts.most_common(k)]
        
        return top_colors
    except:
        return []


def analyze_image_colors(image_path):
    """Analyze image to determine likely flavor based on colors"""
    colors = get_dominant_colors(image_path)
    
    # Convert RGB to color names
    color_analysis = {
        'is_pink': False,
        'is_brown': False,
        'is_chocolate': False,
        'is_white': False,
        'is_golden': False,
        'has_oreo': False,
        'is_strawberry': False
    }
    
    for r, g, b in colors:
        # Pink/Strawberry detection
        if r > 200 and g < 150 and b < 150:
            color_analysis['is_pink'] = True
            color_analysis['is_strawberry'] = True
        
        # Brown/Chocolate detection
        if r < 150 and g < 120 and b < 100:
            color_analysis['is_brown'] = True
            color_analysis['is_chocolate'] = True
            if r > 80 and g > 60:  # Lighter brown = Oreo
                color_analysis['has_oreo'] = True
        
        # White/Vanilla detection
        if r > 200 and g > 200 and b > 200:
            color_analysis['is_white'] = True
        
        # Golden/Caramel detection
        if r > 180 and g > 150 and b < 100:
            color_analysis['is_golden'] = True
    
    return color_analysis


def extract_text_ocr(image_path):
    """Extract text using OCR"""
    if not OCR_AVAILABLE:
        return ""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text.lower()
    except:
        return ""


def identify_with_vision(image_path):
    """Use Gemini Vision API if available"""
    if not VISION_AVAILABLE:
        return None
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        img = Image.open(image_path)
        prompt = """What milkshake or ice cream flavor is this? Identify from these options:
- Oreo Delight (cookies and cream, black/white)
- Strawberry Dream (pink, strawberries)
- Milo Magic (chocolate brown, malt)
- Chocolate Fudge (dark chocolate)
- Caramel Swirl (golden brown, caramel)
- Vegan Vanilla Delight (white, vanilla)
- Jäger Shake (dark amber, alcohol)
- Amarula Bliss (beige-brown, cream liqueur)
- Baileys Berry (pink-cream, berries)
- Espresso Martini Shake (coffee brown)
- Classic Vanilla Cone
- Double Chocolate Cone
- Strawberry Swirl Cone
- Caramel Crunch Cone
- Vegan Chocolate Dream
- Vegan Strawberry Bliss
- Vegan Caramel Swirl

Respond with ONLY the exact name from the list above."""
        
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        print(f"  Vision error: {e}")
        return None


def match_to_menu_item(text, color_analysis, vision_result, menu_items):
    """Match image to menu item"""
    all_text = f"{text} {vision_result or ''}".lower()
    
    scores = {}
    
    for item_id, item_data in menu_items.items():
        score = 0
        title = item_data['title'].lower()
        
        # Vision API match (most reliable)
        if vision_result and title in vision_result.lower():
            score += 50
        
        # Text match
        if title in all_text:
            score += 20
        
        # Color-based matching
        if 'oreo' in title and (color_analysis['has_oreo'] or 'oreo' in all_text):
            score += 15
        if 'strawberry' in title and (color_analysis['is_strawberry'] or 'strawberry' in all_text):
            score += 15
        if 'chocolate' in title and (color_analysis['is_chocolate'] or 'chocolate' in all_text):
            score += 15
        if 'vanilla' in title and (color_analysis['is_white'] or 'vanilla' in all_text):
            score += 15
        if 'caramel' in title and (color_analysis['is_golden'] or 'caramel' in all_text):
            score += 15
        if 'milo' in title and ('milo' in all_text or color_analysis['is_brown']):
            score += 15
        
        # Category-specific
        if 'cone' in title and 'cone' in all_text:
            score += 10
        if 'vegan' in title and 'vegan' in all_text:
            score += 10
        if 'jager' in title or 'jäger' in title:
            if 'jager' in all_text or 'jäger' in all_text:
                score += 15
        if 'amarula' in title and 'amarula' in all_text:
            score += 15
        if 'baileys' in title and 'baileys' in all_text:
            score += 15
        if 'espresso' in title and ('espresso' in all_text or 'coffee' in all_text):
            score += 15
        
        scores[item_id] = score
    
    if scores:
        best_match = max(scores.items(), key=lambda x: x[1])
        if best_match[1] >= 10:
            return best_match[0], best_match[1], scores
    
    return None, 0, scores


def process_images(directory, menu_json="menu_items.json"):
    """Process all images in directory"""
    # Load menu items
    with open(menu_json, 'r') as f:
        data = json.load(f)
    
    menu_items = {}
    for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
        for item in data.get(category, []):
            menu_items[item['id']] = {
                'title': item['title'],
                'category': category
            }
    
    dir_path = Path(directory)
    image_files = [f for f in dir_path.rglob('*') 
                   if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and f.is_file()]
    
    print(f"Processing {len(image_files)} images...\n")
    
    results = []
    
    for img_file in sorted(image_files):
        print(f"Analyzing: {img_file.name}")
        
        # Get analysis
        text = extract_text_ocr(img_file)
        colors = analyze_image_colors(img_file)
        vision = identify_with_vision(img_file)
        
        # Match
        item_id, score, all_scores = match_to_menu_item(text, colors, vision, menu_items)
        
        if item_id:
            new_name = f"{item_id}{img_file.suffix}"
            new_path = img_file.parent / new_name
            
            # Handle duplicates
            counter = 1
            while new_path.exists():
                new_path = img_file.parent / f"{item_id}_{counter}{img_file.suffix}"
                counter += 1
            
            img_file.rename(new_path)
            print(f"  ✓ Renamed to: {new_path.name} ({menu_items[item_id]['title']})")
            results.append({
                'original': img_file.name,
                'new': new_path.name,
                'item': menu_items[item_id]['title'],
                'score': score
            })
        else:
            print(f"  ⚠ Could not identify (top score: {max(all_scores.values()) if all_scores else 0})")
            results.append({
                'original': img_file.name,
                'new': None,
                'score': max(all_scores.values()) if all_scores else 0
            })
    
    # Save results
    results_file = dir_path / "identification_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "GUIDANCE DOCS/100k Shakes Renders"
    
    process_images(directory)
