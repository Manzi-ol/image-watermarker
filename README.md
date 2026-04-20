# Image Watermarker

> Add professional text or logo watermarks to single images or entire folders — powered by **Pillow**.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat)

---

## Features

- **Text watermark** — custom text, any position, adjustable opacity
- **Logo watermark** — overlay a PNG logo, auto-scaled to fit
- **Batch mode** — process an entire folder at once
- 5 positions: `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`
- Drop shadow on text for readability on any background
- Supports JPG, PNG, BMP, WEBP
- Output saved to a separate folder (originals untouched)

---

## Install & Run

```bash
git clone https://github.com/Manzi-ol/image-watermarker
cd image-watermarker
pip install -r requirements.txt
```

---

## Usage

```bash
# Single image — text watermark
python watermarker.py --input photo.jpg --text "© Manzi 2026"

# Custom position & opacity
python watermarker.py --input photo.jpg --text "© Manzi" \
  --position bottom-right --opacity 60

# Logo watermark
python watermarker.py --input photo.jpg --logo logo.png

# Batch — whole folder
python watermarker.py --folder ./photos --text "© Manzi 2026" \
  --output ./watermarked
```

---

## Positions

| Value | Location |
|-------|----------|
| `top-left` | Top left corner |
| `top-right` | Top right corner |
| `bottom-left` | Bottom left corner |
| `bottom-right` | Bottom right corner (default) |
| `center` | Centre of image |

---

## Tech Stack

- **Pillow** — Image manipulation

---

*Part of [Manzi's 100 GitHub Projects Roadmap](https://github.com/Manzi-ol) · Project #22*