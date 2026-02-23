# Setting Up Gemini API Key

## ✅ YES - You Need an API Key!

Gemini runs via Google's API, so you **must** have an API key to use it.

## 🔑 How to Get Your Free API Key

### Step 1: Go to Google AI Studio
Visit: **https://aistudio.google.com/apikey**

### Step 2: Sign In
- Sign in with your Google account
- If you don't have one, create a free Google account

### Step 3: Create API Key
- Click "Create API Key"
- Select "Create API key in new project" (or use existing project)
- Copy your API key immediately (you won't see it again!)

### Step 4: Set Up Your API Key

**Option A: Environment Variable (Recommended)**
```bash
# On Mac/Linux:
export GOOGLE_API_KEY="your-api-key-here"

# On Windows (PowerShell):
$env:GOOGLE_API_KEY="your-api-key-here"

# On Windows (CMD):
set GOOGLE_API_KEY=your-api-key-here
```

**Option B: Pass Directly in Command**
```bash
python generate_images.py --model gemini --gemini-api-key "your-api-key-here"
```

**Option C: Create .env File (Advanced)**
```bash
# Create .env file in project root
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

## 🚀 Quick Start After Getting Key

```bash
# 1. Install Gemini library
pip install google-generativeai pillow numpy

# 2. Set your API key
export GOOGLE_API_KEY="your-api-key-here"

# 3. Test with one image
python generate_by_title.py "Oreo Delight" --model gemini

# 4. Generate all images
python generate_images.py --model gemini
```

## 💰 Free Tier Limits

Google Gemini has a **generous free tier**:
- ✅ Free to start
- ✅ Good for testing and small batches
- ⚠️ Check current limits at: https://ai.google.dev/pricing

For 18 menu items, the free tier should be sufficient!

## 🔒 Security Note

**NEVER commit your API key to Git!**

If you create a `.env` file, add it to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

## ✅ Verify Your Key Works

```bash
# Quick test
python -c "import os; import google.generativeai as genai; genai.configure(api_key=os.getenv('GOOGLE_API_KEY')); print('✓ API Key works!')"
```

## 🆘 Troubleshooting

**"API key not found"**
- Make sure you exported the variable: `echo $GOOGLE_API_KEY`
- Or pass it directly: `--gemini-api-key "your-key"`

**"Invalid API key"**
- Double-check you copied the full key
- Make sure there are no extra spaces
- Try creating a new key

**"Quota exceeded"**
- You've hit the free tier limit
- Wait a bit or check pricing for paid tier
- Consider using Z-Image (local, no limits)



