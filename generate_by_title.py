#!/usr/bin/env python3
"""
Quick helper script to generate images by title
Usage: python generate_by_title.py "Oreo Delight" --model z-image
"""

import json
import sys
from generate_images import ImageGenerator, ZImageGenerator, GeminiGenerator, load_menu_items
import argparse


def find_item_by_title(menu_items: dict, title: str) -> dict:
    """Find menu item by title (case-insensitive)"""
    title_lower = title.lower()
    
    for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
        for item in menu_items.get(category, []):
            if item.get("title", "").lower() == title_lower:
                return item
    
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate image by menu item title")
    parser.add_argument("title", help="Menu item title (e.g., 'Oreo Delight')")
    parser.add_argument("--model", choices=["z-image", "gemini"], default="z-image",
                       help="Image generation model")
    parser.add_argument("--z-image-model", default="Tongyi-MAI/Z-Image-Turbo")
    parser.add_argument("--gemini-api-key", help="Google API key")
    parser.add_argument("--gemini-model", default="gemini-2.0-flash-exp")
    parser.add_argument("--device", default="cuda", help="Device for Z-Image")
    parser.add_argument("--json", default="menu_items.json", help="Path to menu items JSON")
    parser.add_argument("--output", default="images/generated", help="Output directory")
    parser.add_argument("--list", action="store_true", help="List all available titles")
    
    args = parser.parse_args()
    
    # List all titles
    if args.list:
        menu_items = load_menu_items(args.json)
        print("\nAvailable Menu Items:\n")
        for category in ["straightshakes", "shotshakes", "icecream", "vegan"]:
            print(f"\n{category.upper()}:")
            for item in menu_items.get(category, []):
                print(f"  - {item.get('title')}")
        return
    
    # Load menu items
    menu_items = load_menu_items(args.json)
    
    # Find item by title
    item = find_item_by_title(menu_items, args.title)
    
    if not item:
        print(f"Error: Menu item '{args.title}' not found.")
        print("\nUse --list to see all available titles.")
        sys.exit(1)
    
    print(f"Found: {item['title']}")
    print(f"Category: {item.get('category', 'Unknown')}")
    print(f"Prompt: {item['prompt'][:100]}...")
    print()
    
    # Initialize generator
    try:
        if args.model == "z-image":
            generator = ZImageGenerator(
                model_name=args.z_image_model,
                output_dir=args.output,
                device=args.device
            )
        else:
            generator = GeminiGenerator(
                api_key=args.gemini_api_key,
                model_name=args.gemini_model,
                output_dir=args.output
            )
    except Exception as e:
        print(f"Error initializing generator: {e}")
        sys.exit(1)
    
    # Generate image
    filename = f"{item['id']}.png"
    result = generator.generate(item['prompt'], filename)
    
    if result:
        print(f"\n✓ Success! Image saved to: {result}")
    else:
        print("\n✗ Generation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()



