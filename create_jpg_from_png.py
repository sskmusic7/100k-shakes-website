#!/usr/bin/env python3
"""
Create JPG versions of transparent PNGs with solid color backgrounds for menu use
"""
import os
from PIL import Image

# Background colors matching each shake (or use white/cream)
background_colors = {
    "oreo-delight": "#2C1810",  # Deep chocolate
    "strawberry-dream": "#FFF8E7",  # Cream/off-white
    "milo-magic": "#4A2C0A",  # Dark brown
    "jager-shake": "#1A3A1A",  # Forest green
    "amarula-bliss": "#8B5E2A",  # Amber gold
    "strawberry-kiss": "#FFF8E7",  # Cream/off-white
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_jpg_with_background(png_path, jpg_path, bg_color="#FFF8E7"):
    """Create JPG from PNG with solid background color"""
    try:
        # Open PNG with transparency
        img = Image.open(png_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create background
        bg_rgb = hex_to_rgb(bg_color)
        background = Image.new('RGB', img.size, bg_rgb)
        
        # Composite PNG over background
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        
        # Save as JPG (quality 85 for good balance)
        background.save(jpg_path, 'JPEG', quality=85, optimize=True)
        
        original_size = os.path.getsize(png_path) / 1024
        new_size = os.path.getsize(jpg_path) / 1024
        print(f"  ✅ Created: {jpg_path} ({new_size:.1f}KB from {original_size:.1f}KB PNG)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("🖼️  Creating JPG versions with backgrounds for menu...")
    print("=" * 60)
    
    images_dir = "images"
    processed = 0
    
    for base_name, bg_color in background_colors.items():
        png_path = os.path.join(images_dir, f"{base_name}-nobg.png")
        jpg_path = os.path.join(images_dir, f"{base_name}.jpg")
        
        if not os.path.exists(png_path):
            print(f"⚠️  PNG not found: {png_path}")
            continue
        
        print(f"\n🔄 Processing: {base_name}")
        if create_jpg_with_background(png_path, jpg_path, bg_color):
            processed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Done! {processed} JPG files created.")

if __name__ == "__main__":
    main()
