"""Remove background from a raster image and save as PNG with transparency.

Usage:
  python scripts/remove_bg.py path/to/input.jpg path/to/output.png

Requires: `rembg` and `Pillow`.
Install: `pip install rembg pillow`
"""
import sys
from pathlib import Path
from PIL import Image

try:
    from rembg import remove
except Exception:
    raise SystemExit("rembg is required. Install with: pip install rembg pillow")


def remove_background(in_path: Path, out_path: Path):
    with Image.open(in_path) as img:
        result = remove(img)
        result.save(out_path, "PNG")


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/remove_bg.py input.jpg output.png")
        return
    inp = Path(sys.argv[1])
    outp = Path(sys.argv[2])
    if not inp.exists():
        print(f"Input file not found: {inp}")
        return
    outp.parent.mkdir(parents=True, exist_ok=True)
    remove_background(inp, outp)
    print(f"Saved transparent PNG to: {outp}")


if __name__ == "__main__":
    main()
