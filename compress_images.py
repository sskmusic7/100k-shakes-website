#!/usr/bin/env python3
"""
Compress images for web use - reduces file size while maintaining quality
"""

import os
from pathlib import Path
from PIL import Image
import argparse


def compress_image(input_path, output_path, quality=85, max_size=(1200, 1200), format='JPEG'):
    """
    Compress image for web use
    
    Args:
        input_path: Path to input image
        output_path: Path to save compressed image
        quality: JPEG quality (1-100, 85 is good balance)
        max_size: Maximum dimensions (width, height)
        format: Output format ('JPEG' or 'PNG')
    """
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if larger than max_size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save compressed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'JPEG':
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        else:
            img.save(output_path, 'PNG', optimize=True)
        
        # Get file sizes
        original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        return {
            'success': True,
            'original_size_mb': round(original_size, 2),
            'compressed_size_mb': round(compressed_size, 2),
            'reduction_percent': round(reduction, 1)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def compress_directory(input_dir, output_dir, quality=85, max_size=(1200, 1200), format='JPEG'):
    """Compress all images in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return
    
    # Find all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    image_files = [f for f in input_path.iterdir() 
                  if f.suffix.lower() in image_extensions and f.is_file()]
    
    if not image_files:
        print(f"No images found in {input_dir}")
        return
    
    print(f"Found {len(image_files)} images to compress")
    print(f"Output: {output_dir}")
    print(f"Quality: {quality}, Max size: {max_size[0]}x{max_size[1]}\n")
    
    results = []
    total_original = 0
    total_compressed = 0
    
    for img_file in sorted(image_files):
        # Create output filename (change extension if needed)
        if format == 'JPEG':
            output_filename = img_file.stem + '.jpg'
        else:
            output_filename = img_file.name
        
        output_file = output_path / output_filename
        
        print(f"Compressing: {img_file.name}...", end=' ')
        result = compress_image(img_file, output_file, quality, max_size, format)
        
        if result['success']:
            total_original += result['original_size_mb']
            total_compressed += result['compressed_size_mb']
            print(f"✓ {result['original_size_mb']}MB → {result['compressed_size_mb']}MB "
                  f"({result['reduction_percent']}% reduction)")
            results.append({
                'file': img_file.name,
                'output': output_filename,
                **result
            })
        else:
            print(f"✗ Error: {result.get('error', 'Unknown')}")
    
    print(f"\n{'='*60}")
    print(f"Compression Complete!")
    print(f"{'='*60}")
    print(f"Total original size: {round(total_original, 2)} MB")
    print(f"Total compressed size: {round(total_compressed, 2)} MB")
    print(f"Total reduction: {round(((total_original - total_compressed) / total_original) * 100, 1)}%")
    print(f"Files saved to: {output_dir}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Compress images for web use")
    parser.add_argument("--input", default="Brand Assets/100k Shakes gemini renders",
                       help="Input directory")
    parser.add_argument("--output", default="images/compressed",
                       help="Output directory")
    parser.add_argument("--quality", type=int, default=85,
                       help="JPEG quality (1-100, default: 85)")
    parser.add_argument("--max-size", type=int, nargs=2, default=[1200, 1200],
                       help="Maximum dimensions (width height, default: 1200 1200)")
    parser.add_argument("--format", choices=['JPEG', 'PNG'], default='JPEG',
                       help="Output format (default: JPEG)")
    
    args = parser.parse_args()
    
    compress_directory(
        args.input,
        args.output,
        quality=args.quality,
        max_size=tuple(args.max_size),
        format=args.format
    )


if __name__ == "__main__":
    main()
