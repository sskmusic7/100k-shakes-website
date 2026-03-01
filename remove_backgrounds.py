#!/usr/bin/env python3
"""
Remove backgrounds from shake images and save as PNG with transparency.
"""

from rembg import remove
from PIL import Image
import io
import os

# Images needed for the scroll-blend sections
images_to_process = [
    "oreo-delight.jpg",
    "strawberry-dream.jpg",
    "milo-magic.jpg",
    "jager-shake.jpg",
    "amarula-bliss.jpg",
]

images_dir = "images"
output_dir = "images"

print("🎨 Starting background removal...")
print("=" * 50)

for filename in images_to_process:
    input_path = os.path.join(images_dir, filename)
    output_filename = filename.replace(".jpg", "-nobg.png").replace("?v=2", "")
    output_path = os.path.join(output_dir, output_filename)

    if not os.path.exists(input_path):
        print(f"⚠️  Skipping (not found): {input_path}")
        continue

    print(f"🔄 Processing: {filename} → {output_filename}")

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    img.save(output_path, "PNG")

    size_kb = os.path.getsize(output_path) // 1024
    print(f"   ✅ Saved: {output_path} ({size_kb} KB)")

print("=" * 50)
print("✅ Done! All images processed.")
