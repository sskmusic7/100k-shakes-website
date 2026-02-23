#!/usr/bin/env python3
"""
Quick test script to verify Gemini API key is set up correctly
"""

import os
import sys

def test_gemini_setup():
    """Test if Gemini API key is configured"""
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found!")
        print("\nTo set it up:")
        print("  1. Get free API key: https://aistudio.google.com/apikey")
        print("  2. Set environment variable:")
        print("     export GOOGLE_API_KEY='your-key-here'")
        print("\nOr pass it directly:")
        print("  python generate_images.py --model gemini --gemini-api-key 'your-key'")
        return False
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Try importing
    try:
        import google.generativeai as genai
        print("✓ Google Generative AI library installed")
    except ImportError:
        print("❌ ERROR: google-generativeai not installed")
        print("  Install with: pip install google-generativeai")
        return False
    
    # Try configuring
    try:
        genai.configure(api_key=api_key)
        print("✓ API key configured successfully")
        
        # Try creating a model instance (doesn't make API call)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        print("✓ Model instance created")
        print("\n✅ Gemini is ready to use!")
        print("\nTry generating an image:")
        print("  python generate_by_title.py 'Oreo Delight' --model gemini")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - API key not activated")
        print("  - Network connection issue")
        return False

if __name__ == "__main__":
    success = test_gemini_setup()
    sys.exit(0 if success else 1)



