#!/usr/bin/env python3
"""
TIF to multi-format converter
Converts large TIF/TIFF files to more usable formats
NEVER removes original files
"""

import sys
from pathlib import Path

from PIL import Image
import pillow_heif

# Register HEIF/AVIF support
pillow_heif.register_heif_opener()

# Output formats grouped by purpose
FORMATS = {
    "lossless": {
        "ext": ".png",
        "description": "Perfect quality, no artifacts (PNG)",
        "save_args": {"optimize": True},
    },
    "compatible": {
        "ext": ".jpg",
        "description": "Works everywhere, high quality (JPEG 95%)",
        "save_args": {"quality": 95, "optimize": True},
    },
    "balanced": {
        "ext": ".webp",
        "description": "Good quality + small size (WebP 90%)",
        "save_args": {"quality": 90, "method": 6},
    },
    "compact": {
        "ext": ".avif",
        "description": "Smallest files, great for uploads (AVIF 85%)",
        "save_args": {"quality": 85},
    },
}

# Colors for terminal output
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def human_size(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def convert_image(src: Path, output_dirs: dict[str, Path]) -> dict[str, bool]:
    """Convert a single image to all formats."""
    results = {}
    name = src.stem

    try:
        img = Image.open(src)
        # Convert to RGB if necessary (for JPEG/WebP compatibility)
        if img.mode in ("RGBA", "LA", "P"):
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        elif img.mode != "RGB":
            rgb_img = img.convert("RGB")
        else:
            rgb_img = img
    except Exception as e:
        print(f"  {RED}Failed to open: {e}{NC}")
        return {fmt: False for fmt in FORMATS}

    for fmt, settings in FORMATS.items():
        out_path = output_dirs[fmt] / f"{name}{settings['ext']}"

        if out_path.exists():
            print(f"  {fmt} already exists, skipping")
            results[fmt] = True
            continue

        try:
            # Use RGB for lossy formats, original for lossless
            save_img = img if fmt == "lossless" else rgb_img
            save_img.save(out_path, **settings["save_args"])
            size = human_size(out_path.stat().st_size)
            print(f"  {GREEN}{fmt}: {size}{NC}")
            results[fmt] = True
        except Exception as e:
            print(f"  {RED}{fmt}: failed - {e}{NC}")
            results[fmt] = False

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: convert-tif <input-dir> [output-dir]")
        print()
        print("Converts all TIF/TIFF files in <input-dir> to:")
        for fmt, settings in FORMATS.items():
            print(f"  - {settings['description']}")
        print()
        print("Output defaults to <input-dir>, or specify [output-dir].")
        print("Original files are NEVER modified or removed.")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else input_dir

    if not input_dir.is_dir():
        print(f"{RED}Error: '{input_dir}' is not a directory{NC}")
        sys.exit(1)

    # Create output directories
    output_dirs = {}
    for fmt in FORMATS:
        output_dirs[fmt] = output_dir / fmt
        output_dirs[fmt].mkdir(parents=True, exist_ok=True)

    # Find all TIF/TIFF files recursively
    files = list(input_dir.rglob("*.[tT][iI][fF]")) + list(input_dir.rglob("*.[tT][iI][fF][fF]"))

    if not files:
        print(f"{YELLOW}No TIF/TIFF files found in '{input_dir}'{NC}")
        sys.exit(0)

    print(f"{GREEN}Found {len(files)} TIF/TIFF file(s) to convert{NC}")
    print()

    converted = 0
    failed = 0

    for file in sorted(files):
        print(f"{YELLOW}Converting: {file.name}{NC}")
        orig_size = human_size(file.stat().st_size)
        print(f"  Original: {orig_size}")

        results = convert_image(file, output_dirs)

        if all(results.values()):
            converted += 1
        else:
            failed += 1
        print()

    print(f"{GREEN}Done! Converted {converted} file(s){NC}")
    if failed > 0:
        print(f"{YELLOW}{failed} file(s) had errors{NC}")
    print()
    print("Output locations:")
    for fmt, settings in FORMATS.items():
        print(f"  {fmt}/ ({settings['ext'][1:]})")


if __name__ == "__main__":
    main()
