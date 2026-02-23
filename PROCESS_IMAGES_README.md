# Process Gemini Images: Remove Watermark + OCR Labeling

This script processes your Gemini-generated images to:
1. ✅ Remove Gemini logo/watermark from bottom-right corner
2. ✅ Use OCR to identify menu items
3. ✅ Rename files with proper menu item names

## 🚀 Quick Start

### 1. Install Dependencies

**Option A: Tesseract OCR (Recommended - Lighter)**
```bash
# Install Python library
pip install pillow pytesseract numpy

# Install Tesseract OCR binary
# Mac:
brew install tesseract

# Linux:
sudo apt-get install tesseract-ocr

# Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**Option B: PaddleOCR (More Accurate - Heavier)**
```bash
pip install pillow paddlepaddle paddleocr numpy
```

### 2. Run Processing

```bash
# Process all images in the Gemini renders folder
python process_gemini_images.py

# Or specify custom paths
python process_gemini_images.py \
  --input "Brand Assets/100k Shakes gemini renders" \
  --output "images/processed"
```

## 📋 What It Does

### 1. Watermark Removal
- Crops bottom-right corner (15% by default)
- Blurs and blends the area for natural look
- Preserves image quality

### 2. OCR Identification
- Extracts text from images
- Matches text to menu items from `menu_items.json`
- Uses keywords from titles and ingredients

### 3. File Renaming
- Renames files to match menu item IDs
- Example: `Gemini_Generated_Image_xyz.png` → `oreo-delight.png`
- Creates summary JSON with all results

## 📊 Output

Processed images saved to: `images/processed/`

Files renamed to:
- `oreo-delight.png`
- `strawberry-dream.png`
- `jager-shake.png`
- etc.

Summary file: `images/processed/processing_summary.json`

## ⚙️ Options

```bash
# Adjust crop percentage (default: 15%)
python process_gemini_images.py --crop 0.20

# Custom input/output directories
python process_gemini_images.py \
  --input "path/to/gemini/images" \
  --output "path/to/output"
```

## 🔍 How Identification Works

The script:
1. Extracts text from image using OCR
2. Searches for menu item titles in text
3. Matches keywords (ingredients, flavors)
4. Scores matches and picks best match
5. Renames file if confidence score > 3

## 🐛 Troubleshooting

### "Tesseract not found"
```bash
# Mac
brew install tesseract

# Verify installation
tesseract --version
```

### "No OCR engine available"
- Make sure you installed either Tesseract or PaddleOCR
- Check that binaries are in your PATH

### Low identification scores
- Images might not have clear text
- Try PaddleOCR for better accuracy
- Manually check `processing_summary.json` and rename if needed

### Watermark still visible
- Increase crop percentage: `--crop 0.20` (20%)
- The script crops bottom-right corner and blends

## 📝 Manual Review

After processing, check `processing_summary.json`:
```json
[
  {
    "original": "Gemini_Generated_Image_xyz.png",
    "new": "oreo-delight.png",
    "identified": "oreo-delight",
    "score": 15,
    "text": "oreo delight milkshake..."
  }
]
```

If identification is wrong, you can manually rename files.

## 🎯 Next Steps

After processing:
1. Review processed images in `images/processed/`
2. Check `processing_summary.json` for identification results
3. Manually fix any misidentified images
4. Copy to your website's `images/` folder
5. Update HTML to use new filenames


