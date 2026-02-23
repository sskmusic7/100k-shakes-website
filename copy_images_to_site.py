#!/usr/bin/env python3
"""
Copy identified images to website images directory and update HTML files
"""

import os
import shutil
from pathlib import Path
import json

# Menu item IDs that need images
MENU_ITEMS = {
    # StraightShakes
    "oreo-delight": "StraightShake",
    "strawberry-dream": "StraightShake",
    "milo-magic": "StraightShake",
    "chocolate-fudge": "StraightShake",
    "caramel-swirl": "StraightShake",
    "vegan-vanilla-delight": "StraightShake",
    # ShotShakes
    "jager-shake": "ShotShake",
    "amarula-bliss": "ShotShake",
    "baileys-berry": "ShotShake",
    "espresso-martini-shake": "ShotShake",
    # Ice Cream
    "classic-vanilla-cone": "IceCream",
    "double-chocolate-cone": "IceCream",
    "strawberry-swirl-cone": "IceCream",
    "caramel-crunch-cone": "IceCream",
    # Vegan
    "vegan-chocolate-dream": "Vegan",
    "vegan-strawberry-bliss": "Vegan",
    "vegan-caramel-swirl": "Vegan"
}

def find_image_files(base_dir):
    """Find all identified image files"""
    base_path = Path(base_dir)
    images = {}
    
    # Search in all subdirectories
    for ext in ['*.webp', '*.png', '*.jpg', '*.jpeg']:
        for img_file in base_path.rglob(ext):
            name = img_file.stem  # filename without extension
            
            # Check if it matches a menu item ID
            for item_id in MENU_ITEMS.keys():
                if name == item_id or name.startswith(f"{item_id}_"):
                    if item_id not in images:
                        images[item_id] = []
                    images[item_id].append(img_file)
                    break
    
    return images

def copy_best_image(source_files, dest_dir, item_id):
    """Copy the best image (prefer first one, or smallest if multiple)"""
    if not source_files:
        return None
    
    # Use first image (or smallest if we want to optimize)
    source = source_files[0]
    
    # Determine extension
    ext = source.suffix.lower()
    if ext == '.webp':
        ext = '.jpg'  # Convert webp to jpg for better compatibility
    
    dest_file = dest_dir / f"{item_id}{ext}"
    
    # Copy file
    shutil.copy2(source, dest_file)
    return dest_file

def main():
    source_dir = Path("GUIDANCE DOCS/100k Shakes Renders")
    dest_dir = Path("images")
    dest_dir.mkdir(exist_ok=True)
    
    print("Finding images...")
    found_images = find_image_files(source_dir)
    
    print(f"\nFound images for {len(found_images)} menu items:")
    for item_id, files in found_images.items():
        print(f"  {item_id}: {len(files)} image(s)")
    
    print(f"\nCopying images to {dest_dir}...")
    copied = {}
    
    for item_id, files in found_images.items():
        dest_file = copy_best_image(files, dest_dir, item_id)
        if dest_file:
            copied[item_id] = f"images/{dest_file.name}"
            print(f"  ✓ {item_id} → {dest_file.name}")
    
    # Save mapping
    mapping_file = dest_dir / "image_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(copied, f, indent=2)
    
    print(f"\n✓ Copied {len(copied)} images")
    print(f"Mapping saved to: {mapping_file}")
    
    return copied

if __name__ == "__main__":
    main()
