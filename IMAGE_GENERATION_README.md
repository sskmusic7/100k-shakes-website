# 100K Shakes Image Generator

Batch image generation tool for creating menu item photos using AI models.

## 🎨 Supported Models

1. **Z-Image** (Hugging Face) - Recommended for high-quality results
   - Model: `Tongyi-MAI/Z-Image-Turbo`
   - Fast inference (8 steps)
   - Requires GPU (CUDA) for best performance
   - [GitHub](https://github.com/Tongyi-MAI/Z-Image)

2. **Google Gemini 2.5 Flash** - Alternative option
   - Fast generation
   - Requires Google API key
   - Good for quick iterations

## 📦 Installation

### Option 1: Z-Image (Recommended)

```bash
# Install PyTorch (adjust for your CUDA version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install diffusers from source (required for Z-Image support)
pip install git+https://github.com/huggingface/diffusers

# Install other dependencies
pip install pillow numpy
```

### Option 2: Google Gemini

```bash
pip install google-generativeai pillow numpy
```

### Option 3: Install All

```bash
pip install -r requirements_image_gen.txt
pip install git+https://github.com/huggingface/diffusers
```

## 🚀 Quick Start

### Generate All Images (Z-Image)

```bash
python generate_images.py --model z-image
```

### Generate All Images (Gemini)

```bash
# Set your Google API key
export GOOGLE_API_KEY="your-api-key-here"

python generate_images.py --model gemini --gemini-api-key $GOOGLE_API_KEY
```

### Generate Specific Categories

```bash
# Only StraightShakes and ShotShakes
python generate_images.py --model z-image --categories straightshakes shotshakes
```

### Generate Specific Items

```bash
# Generate only Oreo Delight and Strawberry Dream
python generate_images.py --model z-image --items oreo-delight strawberry-dream
```

### Generate Single Image

```bash
python generate_images.py --model z-image --title "Oreo Delight" --prompt "Your custom prompt here"
```

## 📝 JSON File Structure

The `menu_items.json` file contains all menu items with their prompts:

```json
{
  "straightshakes": [
    {
      "id": "oreo-delight",
      "title": "Oreo Delight",
      "category": "StraightShake",
      "prompt": "A luxurious milkshake...",
      "ingredients": [...],
      "tags": ["Popular"]
    }
  ],
  "shotshakes": [...],
  "icecream": [...],
  "vegan": [...]
}
```

## ⚙️ Configuration Options

### Z-Image Options

```bash
python generate_images.py \
  --model z-image \
  --z-image-model "Tongyi-MAI/Z-Image-Turbo" \
  --device cuda \
  --output images/generated
```

### Gemini Options

```bash
python generate_images.py \
  --model gemini \
  --gemini-model "gemini-2.0-flash-exp" \
  --gemini-api-key "your-key" \
  --output images/generated
```

## 📊 Output

Generated images are saved to `images/generated/` by default:
- Filenames match item IDs (e.g., `oreo-delight.png`)
- Format: PNG
- Size: 1024x1024px (Z-Image default)

## 🔧 Advanced Usage

### Custom Output Directory

```bash
python generate_images.py --model z-image --output images/custom
```

### CPU Mode (Z-Image)

If you don't have a GPU:

```bash
python generate_images.py --model z-image --device cpu
```

Note: This will be much slower.

### Using Different Z-Image Models

```bash
# Use base model instead of turbo
python generate_images.py --model z-image --z-image-model "Tongyi-MAI/Z-Image-Base"
```

## 🎯 Tips for Best Results

1. **Z-Image (Recommended)**
   - Use GPU for faster generation
   - Default settings work well (9 steps, guidance_scale=0.0)
   - Images are 1024x1024px by default

2. **Gemini**
   - Good for quick iterations
   - May require prompt adjustments
   - Check API rate limits

3. **Prompt Quality**
   - All prompts in `menu_items.json` are optimized
   - Include "Plain background for menu. Realistic lighting."
   - Mention sticker/logo placement

## 🐛 Troubleshooting

### Z-Image Issues

**Error: "ZImagePipeline not found"**
```bash
# Make sure you installed diffusers from source
pip install git+https://github.com/huggingface/diffusers
```

**Out of Memory**
- Use CPU mode: `--device cpu`
- Or enable CPU offloading in the code
- Reduce image size in code (modify width/height parameters)

### Gemini Issues

**API Key Error**
```bash
# Set environment variable
export GOOGLE_API_KEY="your-key"
# Or pass directly
python generate_images.py --model gemini --gemini-api-key "your-key"
```

**Rate Limits**
- Gemini has API rate limits
- Add delays between requests if needed
- Consider using Z-Image for batch generation

## 📋 Example Workflow

1. **Review prompts** in `menu_items.json`
2. **Test single image**:
   ```bash
   python generate_images.py --model z-image --items oreo-delight
   ```
3. **Generate all StraightShakes**:
   ```bash
   python generate_images.py --model z-image --categories straightshakes
   ```
4. **Generate everything**:
   ```bash
   python generate_images.py --model z-image
   ```
5. **Review images** in `images/generated/`
6. **Update website** with generated images

## 🔗 Resources

- [Z-Image GitHub](https://github.com/Tongyi-MAI/Z-Image)
- [Z-Image Hugging Face](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- [Google Gemini API](https://ai.google.dev/)

## 📝 Notes

- First run will download model weights (several GB for Z-Image)
- Z-Image works best on GPU (CUDA)
- All prompts include branding consistency elements
- Generated images are ready for web use (1024x1024px)



