"""
Debug: save each stage of the current (PNG-based) badge pipeline to assets/testing/
"""

import base64
import io
import os

import requests
from PIL import Image, ImageDraw

URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
TARGET_W = 96
TARGET_H = 28
BG_COLOR = "3178C6"
OUT = "assets/testing"
os.makedirs(OUT, exist_ok=True)

# Stage 1: Raw SVG (for reference)
resp_svg = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
with open(f"{OUT}/01_raw.svg", "wb") as f:
    f.write(resp_svg.content)
print(f"✓ Stage 1: raw SVG ({len(resp_svg.content)} bytes) → 01_raw.svg")

# Stage 2: Raw PNG from shields.io
resp_png = requests.get(URL.replace(".svg", ".png"), timeout=10)
with open(f"{OUT}/02_raw_png.png", "wb") as f:
    f.write(resp_png.content)
orig = Image.open(io.BytesIO(resp_png.content))
print(f"✓ Stage 2: raw PNG from shields.io ({orig.size}, {len(resp_png.content)} bytes) → 02_raw_png.png")

# Stage 3: Calculate scale and resize with LANCZOS
w_ratio = TARGET_W / orig.width
h_ratio = TARGET_H / orig.height
scale = min(w_ratio, h_ratio)
new_w = max(1, int(orig.width * scale))
new_h = max(1, int(orig.height * scale))
print(f"  Scale factors: w={w_ratio:.4f}, h={h_ratio:.4f}, min={scale:.4f}")
print(f"  Resized: {orig.size} → {new_w}x{new_h}")
scaled = orig.resize((new_w, new_h), Image.LANCZOS)
scaled.save(f"{OUT}/03_resized.png", "PNG")
print(f"✓ Stage 3: LANCZOS resized ({new_w}x{new_h}) → 03_resized.png")

# Stage 4: Centered on brand-color canvas
canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (*bytes.fromhex(BG_COLOR), 255))
px = (TARGET_W - new_w) // 2
py = (TARGET_H - new_h) // 2
canvas.paste(scaled, (px, py), scaled.split()[3] if scaled.mode == "RGBA" else None)
canvas.save(f"{OUT}/04_canvas_centered.png", "PNG")
print(f"✓ Stage 4: pasted on canvas at ({px},{py}) → 04_canvas_centered.png")

# Stage 5: Rounded corner mask
mask = Image.new("L", (TARGET_W, TARGET_H), 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle(
    [(0, 0), (TARGET_W - 1, TARGET_H - 1)],
    radius=5,
    fill=255,
)
mask.save(f"{OUT}/05_mask.png")
print(f"✓ Stage 5: rounded mask (rx=5) → 05_mask.png")

# Stage 6: Mask applied to canvas
canvas.putalpha(mask)
canvas.save(f"{OUT}/06_final.png", "PNG")
print(f"✓ Stage 6: final with mask → 06_final.png")

# Stage 7: Base64 encoding (what goes into SVG)
b64 = base64.b64encode(open(f"{OUT}/06_final.png", "rb").read()).decode()
with open(f"{OUT}/07_base64.txt", "w") as f:
    f.write(b64)
print(f"✓ Stage 7: base64 ({len(b64)} chars) → 07_base64.txt")

# Side-by-side comparison: raw SVG rasterized via PIL (as if downloaded as PNG)
# Check actual pixel dimensions vs target
print(f"\n--- Analysis ---")
print(f"Original PNG: {orig.width}x{orig.height}")
print(f"Target:       {TARGET_W}x{TARGET_H}")
print(f"Scale factor: {scale:.4f} ({scale < 1.0 and 'DOWNSCALED' or 'UPSCALED'})")
print(f"Resized to:   {new_w}x{new_h} (to fit within {TARGET_W}x{TARGET_H})")
print(f"Empty space:  top={py}px, bottom={TARGET_H-new_h-py}px, left={px}px, right={TARGET_W-new_w-px}px")
print(f"\nCheck assets/testing/ for each stage.")
