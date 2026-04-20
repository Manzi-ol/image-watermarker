"""
watermarker.py — Add text or image watermarks to photos using Pillow.

Usage:
    python watermarker.py --input photo.jpg --text "© Manzi 2026"
    python watermarker.py --input photo.jpg --text "© Manzi" --position bottom-right --opacity 60
    python watermarker.py --folder ./photos --text "© Manzi 2026" --output ./watermarked
    python watermarker.py --input photo.jpg --logo logo.png
"""

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

POSITIONS = {
    "top-left":     lambda iw, ih, tw, th: (20, 20),
    "top-right":    lambda iw, ih, tw, th: (iw - tw - 20, 20),
    "bottom-left":  lambda iw, ih, tw, th: (20, ih - th - 20),
    "bottom-right": lambda iw, ih, tw, th: (iw - tw - 20, ih - th - 20),
    "center":       lambda iw, ih, tw, th: ((iw - tw) // 2, (ih - th) // 2),
}


def add_text_watermark(
    img: Image.Image,
    text: str,
    position: str = "bottom-right",
    opacity: int = 50,
    font_size: int | None = None,
) -> Image.Image:
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Auto font size: ~4% of image width
    size = font_size or max(20, img.width // 25)
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pos_func = POSITIONS.get(position, POSITIONS["bottom-right"])
    x, y = pos_func(img.width, img.height, tw, th)

    alpha = int(255 * opacity / 100)
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, alpha // 2))  # shadow
    draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))

    combined = Image.alpha_composite(img, overlay)
    return combined.convert("RGB")


def add_logo_watermark(
    img: Image.Image,
    logo_path: str,
    position: str = "bottom-right",
    opacity: int = 60,
    scale: float = 0.15,
) -> Image.Image:
    img = img.convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Scale logo to % of the base image width
    new_w = int(img.width * scale)
    ratio = new_w / logo.width
    new_h = int(logo.height * ratio)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)

    # Apply opacity
    r, g, b, a = logo.split()
    a = a.point(lambda x: int(x * opacity / 100))
    logo.putalpha(a)

    pos_func = POSITIONS.get(position, POSITIONS["bottom-right"])
    x, y = pos_func(img.width, img.height, logo.width, logo.height)

    img.paste(logo, (x, y), logo)
    return img.convert("RGB")


def process_file(src: str, dst: str, args):
    img = Image.open(src)
    if args.logo:
        result = add_logo_watermark(img, args.logo, args.position, args.opacity)
    else:
        result = add_text_watermark(img, args.text, args.position, args.opacity)
    result.save(dst, quality=95)
    print(f"  Saved: {dst}")


def main():
    parser = argparse.ArgumentParser(description="Image Watermarker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input",  help="Single image file")
    group.add_argument("--folder", help="Folder of images")

    parser.add_argument("--text",     default="", help="Watermark text")
    parser.add_argument("--logo",     default="", help="Path to logo image")
    parser.add_argument("--position", default="bottom-right",
                        choices=list(POSITIONS.keys()), help="Watermark position")
    parser.add_argument("--opacity",  type=int, default=50,  help="Opacity 0-100")
    parser.add_argument("--output",   default="watermarked", help="Output folder")
    args = parser.parse_args()

    if not args.text and not args.logo:
        parser.error("Provide --text or --logo")

    os.makedirs(args.output, exist_ok=True)

    if args.input:
        name = Path(args.input).stem
        ext  = Path(args.input).suffix
        dst  = os.path.join(args.output, f"{name}_watermarked{ext}")
        process_file(args.input, dst, args)

    elif args.folder:
        files = [
            f for f in os.listdir(args.folder)
            if Path(f).suffix.lower() in SUPPORTED
        ]
        print(f"\n  Processing {len(files)} image(s) from '{args.folder}' …\n")
        for f in files:
            src = os.path.join(args.folder, f)
            dst = os.path.join(args.output, f)
            process_file(src, dst, args)
        print(f"\n  Done! Output saved to '{args.output}'\n")


if __name__ == "__main__":
    main()
