#!/usr/bin/env python3
"""
Identify images using Google Vision API for accurate identification
"""

import os
import json
from pathlib import Path
from PIL import Image
import google.generativeai as genai

# Set API key
API_KEY = "AIzaSyAY6rBnvQ5uFMvjJsgrKxX8v1zTsYd-wEk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def load_menu_items(json_path="menu_items.json"):
    """Load menu items"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    menu_items = {}
    all_items = []
    
    for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
        for item in data.get(category, []):
            menu_items[item['id']] = {
                'title': item['title'],
                'category': category
            }
            all_items.append(item['title'])
    
    return menu_items, all_items

def identify_image(image_path, all_items):
    """Identify image using Vision API"""
    try:
        img = Image.open(image_path)
        
        prompt = f"""Identify this milkshake or ice cream image. Choose the EXACT name from this list:

{', '.join(all_items)}

Respond with ONLY the exact name from the list above, nothing else."""
        
        print(f"  Analyzing with Vision API...")
        response = model.generate_content([prompt, img])
        result = response.text.strip()
        
        # Clean up response
        result = result.split('\n')[0].strip()
        result = result.split('.')[0].strip()  # Remove numbering
        result = result.replace('"', '').replace("'", "")
        
        print(f"  Vision result: {result}")
        return result
        
    except Exception as e:
        print(f"  Vision API error: {e}")
        return None

def find_menu_item_id(title, menu_items):
    """Find menu item ID from title"""
    title_lower = title.lower()
    for item_id, item_data in menu_items.items():
        if item_data['title'].lower() == title_lower:
            return item_id
        # Partial match
        if title_lower in item_data['title'].lower() or item_data['title'].lower() in title_lower:
            return item_id
    return None

def process_folder(folder_path, menu_json="menu_items.json"):
    """Process all images in folder"""
    menu_items, all_items = load_menu_items(menu_json)
    folder = Path(folder_path)
    
    images = [f for f in folder.rglob('*') 
              if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and f.is_file()]
    
    print(f"\n{'='*60}")
    print(f"Processing {len(images)} images in: {folder.name}")
    print(f"{'='*60}\n")
    
    results = []
    
    for img in sorted(images):
        print(f"{img.name}")
        
        # Use Vision API
        vision_result = identify_image(img, all_items)
        
        if vision_result:
            item_id = find_menu_item_id(vision_result, menu_items)
            
            if item_id:
                new_name = f"{item_id}{img.suffix}"
                new_path = img.parent / new_name
                
                # Handle duplicates
                counter = 1
                while new_path.exists():
                    new_path = img.parent / f"{item_id}_{counter}{img.suffix}"
                    counter += 1
                
                img.rename(new_path)
                print(f"  ✓ → {new_path.name} ({menu_items[item_id]['title']})")
                results.append({
                    'original': img.name,
                    'new': new_path.name,
                    'item': menu_items[item_id]['title'],
                    'vision_result': vision_result
                })
            else:
                print(f"  ⚠ Could not match: {vision_result}")
                results.append({
                    'original': img.name,
                    'new': None,
                    'vision_result': vision_result
                })
        else:
            print(f"  ✗ Vision API failed")
            results.append({
                'original': img.name,
                'new': None,
                'error': 'Vision API failed'
            })
    
    # Save results
    results_file = folder / "vision_identification_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    return results

if __name__ == "__main__":
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
