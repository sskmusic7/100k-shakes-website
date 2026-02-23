# Quick Start: Image Generation

## 🚀 Fastest Way to Generate All Images

### Using Z-Image (Recommended - Best Quality)

```bash
# 1. Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install git+https://github.com/huggingface/diffusers
pip install pillow numpy

# 2. Generate all images
python generate_images.py --model z-image
```

### Using Google Gemini (Faster Setup)

```bash
# 1. Install dependencies
pip install google-generativeai pillow numpy

# 2. Set API key
export GOOGLE_API_KEY="your-api-key-here"

# 3. Generate all images
python generate_images.py --model gemini
```

## 🎯 Generate by Title

```bash
# List all available titles
python generate_by_title.py --list

# Generate specific item by title
python generate_by_title.py "Oreo Delight" --model z-image
python generate_by_title.py "Jäger Shake" --model gemini
```

## 📦 What Gets Generated

All 18 menu items:
- 6 StraightShakes
- 4 ShotShakes  
- 4 Ice Cream Cones
- 4 Vegan Options (3 unique + 1 duplicate)

Images saved to: `images/generated/`

## ⚡️ Quick Examples

```bash
# Generate just StraightShakes
python generate_images.py --model z-image --categories straightshakes

# Generate just one item
python generate_by_title.py "Strawberry Dream" --model z-image

# Generate specific items by ID
python generate_images.py --model z-image --items oreo-delight milo-magic
```

## 🔧 Troubleshooting

**Z-Image not working?**
```bash
# Make sure diffusers is from source
pip install git+https://github.com/huggingface/diffusers --upgrade
```

**Out of GPU memory?**
```bash
# Use CPU (slower but works)
python generate_images.py --model z-image --device cpu
```

**Gemini API key?**
Get one at: https://ai.google.dev/



