"""
Debug: save each stage of badge processing to assets/testing/
"""

import base64
import io
import os

import cairosvg
import requests
from PIL import Image, ImageDraw

TARGET_W = 96
TARGET_H = 28
BG_COLOR = "3178C6"
URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
OUT = "assets/testing"
os.makedirs(OUT, exist_ok=True)

# Stage 1: Raw SVG from shields.io
resp = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
svg_raw = resp.content
with open(f"{OUT}/01_raw.svg", "wb") as f:
    f.write(svg_raw)
print(f"✓ Stage 1: raw SVG ({len(svg_raw)} bytes) → 01_raw.svg")

# Stage 2: Rasterize at 1x
png_1x = cairosvg.svg2png(bytestring=svg_raw, output_width=TARGET_W, output_height=TARGET_H)
with open(f"{OUT}/02_rasterized_1x.png", "wb") as f:
    f.write(png_1x)
print(f"✓ Stage 2: rasterized 1x ({len(png_1x)} bytes) → 02_rasterized_1x.png")

# Stage 3: Rasterize at 2x
png_2x = cairosvg.svg2png(bytestring=svg_raw, output_width=TARGET_W * 2, output_height=TARGET_H * 2)
with open(f"{OUT}/03_rasterized_2x.png", "wb") as f:
    f.write(png_2x)
print(f"✓ Stage 3: rasterized 2x ({len(png_2x)} bytes) → 03_rasterized_2x.png")

# Stage 4: Downscale 2x → target with LANCZOS
img = Image.open(io.BytesIO(png_2x)).convert("RGBA")
img_small = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
with open(f"{OUT}/04_downscaled.png", "wb") as f:
    img_small.save(f, "PNG")
print(f"✓ Stage 4: downscaled ({img.width}x{img.height} → {img_small.width}x{img_small.height}) → 04_downscaled.png")

# Stage 5: Centered on bg canvas
canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (*bytes.fromhex(BG_COLOR), 255))
px = (TARGET_W - img_small.width) // 2
py = (TARGET_H - img_small.height) // 2
canvas.paste(img_small, (px, py), img_small)
with open(f"{OUT}/05_canvas_centered.png", "wb") as f:
    canvas.save(f, "PNG")
print(f"✓ Stage 5: centered on canvas (paste at {px},{py}) → 05_canvas_centered.png")

# Stage 6: Rounded corner mask applied
mask = Image.new("L", (TARGET_W, TARGET_H), 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle([(0, 0), (TARGET_W - 1, TARGET_H - 1)], radius=5, fill=255)
mask.save(f"{OUT}/06_mask.png")
print(f"✓ Stage 6: mask → 06_mask.png")

canvas.putalpha(mask)
with open(f"{OUT}/07_final.png", "wb") as f:
    canvas.save(f, "PNG")
print(f"✓ Stage 7: final → 07_final.png")

# Stage 8: base64 check
with open(f"{OUT}/07_final.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
with open(f"{OUT}/08_base64.txt", "w") as f:
    f.write(b64)
print(f"✓ Stage 8: base64 ({len(b64)} chars) → 08_base64.txt")

print("\nDone. Check assets/testing/ for each stage.")
