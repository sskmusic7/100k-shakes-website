#!/usr/bin/env python3
"""
100K Shakes Batch Image Generator
Supports Z-Image (Hugging Face) and Google Gemini 2.5 Flash
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Try importing required libraries
try:
    import torch
    from PIL import Image
    Z_IMAGE_AVAILABLE = True
except ImportError:
    Z_IMAGE_AVAILABLE = False
    print("Warning: PyTorch/PIL not available. Z-Image generation disabled.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Generative AI not available. Gemini generation disabled.")


class ImageGenerator:
    """Base class for image generation"""
    
    def __init__(self, output_dir: str = "images/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, prompt: str, filename: str, **kwargs) -> Optional[str]:
        """Generate image from prompt. Returns path to saved image or None."""
        raise NotImplementedError


class ZImageGenerator(ImageGenerator):
    """
    Z-Image generator using Hugging Face
    
    ⚠️ IMPORTANT: This runs LOCALLY on your machine!
    - Downloads model weights (~6GB) to your computer
    - Runs inference on your GPU (CUDA) or CPU
    - NO API calls - completely local/offline after download
    - Requires: GPU with CUDA (recommended) or CPU (slower)
    """
    
    def __init__(self, model_name: str = "Tongyi-MAI/Z-Image-Turbo", output_dir: str = "images/generated", device: str = "cuda"):
        super().__init__(output_dir)
        if not Z_IMAGE_AVAILABLE:
            raise ImportError("Z-Image requires: pip install torch pillow diffusers")
        
        self.device = device
        self.model_name = model_name
        self.pipe = None
        self._load_model()
    
    def _load_model(self):
        """Load Z-Image pipeline"""
        try:
            from diffusers import ZImagePipeline
            print(f"Loading Z-Image model: {self.model_name}")
            self.pipe = ZImagePipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=False,
            )
            self.pipe.to(self.device)
            print("✓ Z-Image model loaded successfully")
        except Exception as e:
            print(f"Error loading Z-Image: {e}")
            print("Make sure you have installed: pip install git+https://github.com/huggingface/diffusers")
            raise
    
    def generate(self, prompt: str, filename: str, num_steps: int = 9, guidance_scale: float = 0.0, 
                 width: int = 1024, height: int = 1024, seed: Optional[int] = None) -> Optional[str]:
        """Generate image using Z-Image"""
        if self.pipe is None:
            return None
        
        try:
            generator = torch.Generator(self.device)
            if seed is not None:
                generator.manual_seed(seed)
            
            print(f"Generating: {filename}")
            image = self.pipe(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=num_steps,
                guidance_scale=guidance_scale,
                generator=generator,
            ).images[0]
            
            output_path = self.output_dir / filename
            image.save(output_path)
            print(f"✓ Saved: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"✗ Error generating {filename}: {e}")
            return None


class GeminiGenerator(ImageGenerator):
    """
    Google Gemini 2.5 Flash generator
    
    ⚠️ IMPORTANT: This runs via API (cloud-based)!
    - Sends requests to Google's servers
    - Requires internet connection
    - Requires Google API key (free tier available)
    - No local model download - runs on Google's servers
    - Subject to API rate limits and costs
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp", 
                 output_dir: str = "images/generated"):
        super().__init__(output_dir)
        if not GEMINI_AVAILABLE:
            raise ImportError("Gemini requires: pip install google-generativeai")
        
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google API key required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"✓ Gemini model initialized: {model_name} (API-based)")
    
    def generate(self, prompt: str, filename: str, **kwargs) -> Optional[str]:
        """Generate image using Gemini"""
        try:
            print(f"Generating: {filename}")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="image/png",
                )
            )
            
            if hasattr(response, 'image') and response.image:
                output_path = self.output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(response.image)
                print(f"✓ Saved: {output_path}")
                return str(output_path)
            else:
                print(f"✗ No image in response for {filename}")
                return None
        except Exception as e:
            print(f"✗ Error generating {filename}: {e}")
            return None


def load_menu_items(json_path: str = "menu_items.json") -> Dict:
    """Load menu items from JSON file"""
    with open(json_path, 'r') as f:
        return json.load(f)


def generate_all_images(generator: ImageGenerator, menu_items: Dict, 
                       categories: Optional[List[str]] = None, 
                       item_ids: Optional[List[str]] = None):
    """Generate images for all menu items"""
    if categories is None:
        categories = ["straightshakes", "shotshakes", "icecream", "vegan"]
    
    total = 0
    success = 0
    
    for category in categories:
        if category not in menu_items:
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {category.upper()}")
        print(f"{'='*60}")
        
        for item in menu_items[category]:
            item_id = item.get("id", item.get("title", "").lower().replace(" ", "-"))
            
            # Skip if item_ids filter is specified
            if item_ids and item_id not in item_ids:
                continue
            
            title = item.get("title", "Unknown")
            prompt = item.get("prompt", "")
            
            if not prompt:
                print(f"⚠ Skipping {title}: No prompt found")
                continue
            
            # Generate filename
            filename = f"{item_id}.png"
            
            total += 1
            result = generator.generate(prompt, filename)
            if result:
                success += 1
    
    print(f"\n{'='*60}")
    print(f"Generation Complete: {success}/{total} successful")
    print(f"{'='*60}")


def generate_single_image(generator: ImageGenerator, title: str, prompt: str, filename: Optional[str] = None):
    """Generate a single image by title"""
    if filename is None:
        filename = f"{title.lower().replace(' ', '-')}.png"
    
    return generator.generate(prompt, filename)


def main():
    parser = argparse.ArgumentParser(description="100K Shakes Batch Image Generator")
    parser.add_argument("--model", choices=["z-image", "gemini"], default="z-image",
                       help="Image generation model to use")
    parser.add_argument("--z-image-model", default="Tongyi-MAI/Z-Image-Turbo",
                       help="Z-Image model name")
    parser.add_argument("--gemini-model", default="gemini-2.0-flash-exp",
                       help="Gemini model name")
    parser.add_argument("--gemini-api-key", help="Google API key (or set GOOGLE_API_KEY env var)")
    parser.add_argument("--device", default="cuda", help="Device for Z-Image (cuda/cpu)")
    parser.add_argument("--json", default="menu_items.json", help="Path to menu items JSON")
    parser.add_argument("--categories", nargs="+", 
                       choices=["straightshakes", "shotshakes", "icecream", "vegan"],
                       help="Categories to generate (default: all)")
    parser.add_argument("--items", nargs="+", help="Specific item IDs to generate")
    parser.add_argument("--output", default="images/generated", help="Output directory")
    parser.add_argument("--title", help="Generate single image by title")
    parser.add_argument("--prompt", help="Prompt for single image generation")
    
    args = parser.parse_args()
    
    # Initialize generator
    try:
        if args.model == "z-image":
            if not Z_IMAGE_AVAILABLE:
                print("Error: Z-Image not available. Install with: pip install torch pillow diffusers")
                sys.exit(1)
            generator = ZImageGenerator(
                model_name=args.z_image_model,
                output_dir=args.output,
                device=args.device
            )
        elif args.model == "gemini":
            if not GEMINI_AVAILABLE:
                print("Error: Gemini not available. Install with: pip install google-generativeai")
                sys.exit(1)
            generator = GeminiGenerator(
                api_key=args.gemini_api_key,
                model_name=args.gemini_model,
                output_dir=args.output
            )
        else:
            print(f"Unknown model: {args.model}")
            sys.exit(1)
    except Exception as e:
        print(f"Error initializing generator: {e}")
        sys.exit(1)
    
    # Single image generation
    if args.title and args.prompt:
        generate_single_image(generator, args.title, args.prompt)
        return
    
    # Batch generation from JSON
    if not os.path.exists(args.json):
        print(f"Error: JSON file not found: {args.json}")
        sys.exit(1)
    
    menu_items = load_menu_items(args.json)
    generate_all_images(generator, menu_items, args.categories, args.items)


if __name__ == "__main__":
    main()

