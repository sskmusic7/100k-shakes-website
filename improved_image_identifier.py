#!/usr/bin/env python3
"""
Improved image identifier that uses folder context and better matching
"""

import os
import json
from pathlib import Path
from PIL import Image

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    import google.generativeai as genai
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False


def get_folder_context(folder_path):
    """Determine category hints from folder name"""
    folder_name = Path(folder_path).name.lower()
    context = {
        'is_vegan': 'vegan' in folder_name,
        'is_cone': 'cone' in folder_name or 'icecream' in folder_name,
        'is_shotshake': 'shot' in folder_name,
        'is_straightshake': 'straight' in folder_name or 'z image' in folder_name
    }
    return context


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
    """Use Gemini Vision API"""
    if not VISION_AVAILABLE:
        return None
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        img = Image.open(image_path)
        prompt = """Identify this milkshake/ice cream from these exact options (respond with ONLY the name):

StraightShakes:
- Oreo Delight
- Strawberry Dream  
- Milo Magic
- Chocolate Fudge
- Caramel Swirl
- Vegan Vanilla Delight

ShotShakes:
- Jäger Shake
- Amarula Bliss
- Baileys Berry
- Espresso Martini Shake

Ice Cream Cones:
- Classic Vanilla Cone
- Double Chocolate Cone
- Strawberry Swirl Cone
- Caramel Crunch Cone

Vegan:
- Vegan Chocolate Dream
- Vegan Strawberry Bliss
- Vegan Caramel Swirl

Respond with ONLY the exact name from above."""
        
        response = model.generate_content([prompt, img])
        result = response.text.strip()
        # Clean up response
        for line in result.split('\n'):
            line = line.strip()
            if any(item in line for item in ['Oreo', 'Strawberry', 'Milo', 'Chocolate', 'Caramel', 'Vanilla', 'Jäger', 'Amarula', 'Baileys', 'Espresso', 'Cone', 'Vegan']):
                return line
        return result
    except Exception as e:
        return None


def match_to_menu(text, vision_result, folder_context, menu_items):
    """Match with folder context"""
    all_text = f"{text} {vision_result or ''}".lower()
    
    scores = {}
    
    for item_id, item_data in menu_items.items():
        score = 0
        title = item_data['title'].lower()
        category = item_data['category'].lower()
        
        # Vision API match (most reliable - 100 points)
        if vision_result:
            vision_lower = vision_result.lower()
            if title in vision_lower:
                score += 100
            elif any(word in vision_lower for word in title.split()):
                score += 50
        
        # Folder context matching (strong hint)
        if folder_context['is_vegan'] and 'vegan' in category:
            score += 30
        if folder_context['is_cone'] and 'icecream' in category:
            score += 30
        if folder_context['is_shotshake'] and 'shotshake' in category:
            score += 30
        if folder_context['is_straightshake'] and 'straightshake' in category:
            score += 30
        
        # Text matching
        if title in all_text:
            score += 20
        
        # Keyword matching
        keywords = {
            'oreo': ['oreo', 'cookie', 'cookies and cream'],
            'strawberry': ['strawberry', 'pink'],
            'milo': ['milo', 'malt'],
            'chocolate': ['chocolate', 'fudge'],
            'caramel': ['caramel', 'toffee'],
            'vanilla': ['vanilla', 'white'],
            'jager': ['jager', 'jäger', 'jagermeister'],
            'amarula': ['amarula'],
            'baileys': ['baileys', 'irish cream'],
            'espresso': ['espresso', 'coffee', 'martini']
        }
        
        for key, terms in keywords.items():
            if key in title:
                for term in terms:
                    if term in all_text:
                        score += 15
        
        scores[item_id] = score
    
    if scores:
        best = max(scores.items(), key=lambda x: x[1])
        if best[1] >= 15:  # Lower threshold
            return best[0], best[1], scores
    
    return None, 0, scores


def process_folder(folder_path, menu_json="menu_items.json"):
    """Process images in a folder"""
    # Load menu
    with open(menu_json, 'r') as f:
        data = json.load(f)
    
    menu_items = {}
    for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
        for item in data.get(category, []):
            menu_items[item['id']] = {
                'title': item['title'],
                'category': category
            }
    
    folder = Path(folder_path)
    folder_context = get_folder_context(folder_path)
    
    images = [f for f in folder.rglob('*') 
              if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and f.is_file()]
    
    print(f"\n{'='*60}")
    print(f"Processing {len(images)} images in: {folder.name}")
    print(f"Context: {folder_context}")
    print(f"{'='*60}\n")
    
    results = []
    
    for img in sorted(images):
        print(f"{img.name}")
        
        text = extract_text_ocr(img)
        vision = identify_with_vision(img)
        
        if vision:
            print(f"  Vision: {vision}")
        
        item_id, score, all_scores = match_to_menu(text, vision, folder_context, menu_items)
        
        if item_id:
            new_name = f"{item_id}{img.suffix}"
            new_path = img.parent / new_name
            
            counter = 1
            while new_path.exists():
                new_path = img.parent / f"{item_id}_{counter}{img.suffix}"
                counter += 1
            
            img.rename(new_path)
            print(f"  ✓ → {new_path.name} ({menu_items[item_id]['title']}, score: {score})")
            results.append({
                'original': img.name,
                'new': new_path.name,
                'item': menu_items[item_id]['title'],
                'score': score
            })
        else:
            top_score = max(all_scores.values()) if all_scores else 0
            print(f"  ⚠ Could not identify (top score: {top_score})")
            results.append({
                'original': img.name,
                'new': None,
                'score': top_score
            })
    
    # Save results
    results_file = folder / "identification_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results


if __name__ == "__main__":
    import sys
    
    base = "GUIDANCE DOCS/100k Shakes Renders"
    
    folders = [
        f"{base}/Z Image Renders",
        f"{base}/Z Image Renders/Shot Shakes",
        f"{base}/Vegan Delights",
        f"{base}/Icecream cones"
    ]
    
    for folder in folders:
        if Path(folder).exists():
            process_folder(folder)
