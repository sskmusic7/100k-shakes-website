#!/usr/bin/env python3
"""
Process new transparent PNG images: compress and rename for web use
"""
import os
from PIL import Image
import shutil

# Source directory
source_dir = "images/NEW UPLOADED IMAGES 100KSHAKES"
target_dir = "images"

# Mapping: (source filename pattern, target filename)
# Using the (2) versions as they're smaller
image_mapping = [
    ("Amarula Bliss (2).png", "amarula-bliss-nobg.png"),
    ("Jäger Shake (2).png", "jager-shake-nobg.png"),
    ("Milo Magc (2).png", "milo-magic-nobg.png"),  # Note: fixing typo "Magc" -> "magic"
    ("Oreo Delight (2).png", "oreo-delight-nobg.png"),
    ("Strawberry Dream (2).png", "strawberry-dream-nobg.png"),
    ("Strawberry Kiss (With Strawberry Lips) (2).png", "strawberry-kiss-nobg.png"),
]

def compress_png(input_path, output_path, max_size_kb=500, quality=85):
    """
    Compress PNG while maintaining transparency.
    Tries to reduce file size by optimizing and potentially converting to WebP if needed.
    """
    try:
        img = Image.open(input_path)
        
        # Ensure we're working with RGBA for transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get original size
        original_size = os.path.getsize(input_path) / 1024  # KB
        
        # First, try saving as optimized PNG
        img.save(output_path, 'PNG', optimize=True, compress_level=9)
        new_size = os.path.getsize(output_path) / 1024
        
        print(f"  📦 Compressed: {original_size:.1f}KB → {new_size:.1f}KB")
        
        # If still too large, try WebP (but keep PNG for transparency compatibility)
        if new_size > max_size_kb:
            webp_path = output_path.replace('.png', '.webp')
            img.save(webp_path, 'WEBP', quality=quality, method=6)
            webp_size = os.path.getsize(webp_path) / 1024
            print(f"  🌐 Also created WebP: {webp_size:.1f}KB")
            return webp_path
        
        return output_path
        
    except Exception as e:
        print(f"  ❌ Error compressing {input_path}: {e}")
        return None

def main():
    print("🎨 Processing new transparent PNG images...")
    print("=" * 60)
    
    if not os.path.exists(source_dir):
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    processed = 0
    for source_pattern, target_name in image_mapping:
        source_path = os.path.join(source_dir, source_pattern)
        target_path = os.path.join(target_dir, target_name)
        
        if not os.path.exists(source_path):
            print(f"⚠️  Not found: {source_pattern}")
            continue
        
        print(f"\n🔄 Processing: {source_pattern}")
        print(f"   → {target_name}")
        
        result = compress_png(source_path, target_path)
        if result:
            processed += 1
            print(f"   ✅ Saved: {target_path}")
    
    print("\n" + "=" * 60)
    print(f"✅ Done! {processed} images processed.")
    
    # Also copy the backdrop image if needed
    backdrop_source = os.path.join(source_dir, "BACKDROP IMAGE.png")
    if os.path.exists(backdrop_source):
        print(f"\n📸 Backdrop image found (not processed - too large for web)")
        print(f"   Location: {backdrop_source}")

if __name__ == "__main__":
    main()
