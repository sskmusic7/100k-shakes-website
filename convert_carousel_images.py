#!/usr/bin/env python3
"""
Convert the full background versions of shake images for carousel use.
These are the styled shots with bottles, ingredients, and props.
"""
import os
from PIL import Image

source_dir = "images/NEW UPLOADED IMAGES 100KSHAKES"
target_dir = "images"

# Map: source filename → target filename (for carousel)
image_mapping = [
    ("Oreo Delight.png", "oreo-delight.jpg"),
    ("Strawberry Dream.png", "strawberry-dream.jpg"),
    ("Milo Magc.png", "milo-magic.jpg"),
    ("Jäger Shake.png", "jager-shake.jpg"),
    ("Amarula Bliss.png", "amarula-bliss.jpg"),
    ("Strawberry Kiss (With Strawberry Lips).png", "strawberry-kiss.jpg"),
]

def convert_to_jpg(input_path, output_path, quality=85):
    """Convert PNG to compressed JPG for web carousel"""
    try:
        img = Image.open(input_path)
        # Convert RGBA to RGB (JPG doesn't support transparency)
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as optimized JPG
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        original_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        print(f"  ✅ {original_size:.0f}KB → {new_size:.0f}KB")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("🖼️  Converting full background images for carousel...")
    print("=" * 60)
    
    processed = 0
    for source_name, target_name in image_mapping:
        source_path = os.path.join(source_dir, source_name)
        target_path = os.path.join(target_dir, target_name)
        
        if not os.path.exists(source_path):
            print(f"⚠️  Not found: {source_name}")
            continue
        
        print(f"\n🔄 {source_name} → {target_name}")
        if convert_to_jpg(source_path, target_path):
            processed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Done! {processed} carousel images created.")

if __name__ == "__main__":
    main()
