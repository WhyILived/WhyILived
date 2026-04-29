"""
Debug: test different rasterization methods on the raw SVG.
"""

import base64
import io
import os

import requests
from PIL import Image, ImageDraw

OUT = "assets/testing"

URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
resp = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
svg_raw = resp.content

# Method 1: cairosvg at 1x
try:
    import cairosvg
    png = cairosvg.svg2png(bytestring=svg_raw, output_width=96, output_height=28)
    with open(f"{OUT}/m1_cairo_96x28.png", "wb") as f:
        f.write(png)
    img = Image.open(io.BytesIO(png))
    print(f"✓ Method 1: cairosvg 96x28 → m1_cairo_96x28.png ({img.size})")
except Exception as e:
    print(f"✗ Method 1: cairosvg → {e}")

# Method 2: cairosvg at 2x, then downscale
try:
    import cairosvg
    png = cairosvg.svg2png(bytestring=svg_raw, output_width=192, output_height=56)
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    img = img.resize((96, 28), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    with open(f"{OUT}/m2_cairo_2x_lanczos.png", "wb") as f:
        f.write(buf.getvalue())
    print(f"✓ Method 2: cairosvg 2x+LANCZOS → m2_cairo_2x_lanczos.png")
except Exception as e:
    print(f"✗ Method 2: cairosvg 2x → {e}")

# Method 3: Use the PNG directly from shields.io (which is pre-rasterized)
try:
    url_png = URL.replace(".svg", ".png")
    resp = requests.get(url_png, timeout=10)
    img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
    # Scale up to ensure quality, then to target
    # First get original dimensions
    orig_w, orig_h = img.size
    print(f"  Original PNG: {orig_w}x{orig_h}")
    # Scale to 4x target, then down to target
    scale_4x = img.resize((96 * 4, 28 * 4), Image.LANCZOS)
    scale_target = scale_4x.resize((96, 28), Image.LANCZOS)
    buf = io.BytesIO()
    scale_target.save(buf, "PNG")
    with open(f"{OUT}/m3_png_4x_lanczos.png", "wb") as f:
        f.write(buf.getvalue())
    print(f"✓ Method 3: PNG → 4x → LANCZOS → m3_png_4x_lanczos.png")
except Exception as e:
    print(f"✗ Method 3: PNG upscaling → {e}")

# Method 4: PNG original scaled directly with LANCZOS
try:
    url_png = URL.replace(".svg", ".png")
    resp = requests.get(url_png, timeout=10)
    img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
    img_target = img.resize((96, 28), Image.LANCZOS)
    buf = io.BytesIO()
    img_target.save(buf, "PNG")
    with open(f"{OUT}/m4_png_direct.png", "wb") as f:
        f.write(buf.getvalue())
    print(f"✓ Method 4: PNG direct LANCZOS → m4_png_direct.png")
except Exception as e:
    print(f"✗ Method 4: PNG direct → {e}")

# Method 5: PNG with NEAREST resampling (no interpolation artifacts)
try:
    url_png = URL.replace(".svg", ".png")
    resp = requests.get(url_png, timeout=10)
    img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
    # Use LANCZOS but at exact integer scale
    # First determine the integer multiplier needed
    scale_w = 96 / img.width
    scale_h = 28 / img.height
    print(f"  Scale factors: w={scale_w:.3f} h={scale_h:.3f}")
    img_target = img.resize((96, 28), Image.LANCZOS)
    buf = io.BytesIO()
    img_target.save(buf, "PNG")
    with open(f"{OUT}/m5_png_lanczos.png", "wb") as f:
        f.write(buf.getvalue())
    print(f"✓ Method 5: PNG LANCZOS → m5_png_lanczos.png")
except Exception as e:
    print(f"✗ Method 5: PNG LANCZOS → {e}")

# Method 6: PNG with Image.Resampling.LANCZOS + quality check
try:
    url_png = URL.replace(".svg", ".png")
    resp = requests.get(url_png, timeout=10)
    img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
    print(f"  PNG raw: {img.size}, mode={img.mode}")
    # Resize maintaining aspect ratio, then pad
    target_w, target_h = 96, 28
    w_ratio = target_w / img.width
    h_ratio = target_h / img.height
    scale = min(w_ratio, h_ratio)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    scaled = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (target_w, target_h), (0x31, 0x78, 0xC6, 255))
    px = (target_w - new_w) // 2
    py = (target_h - new_h) // 2
    canvas.paste(scaled, (px, py), scaled)
    # Rounded rect mask
    mask = Image.new("L", (target_w, target_h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (target_w - 1, target_h - 1)], radius=5, fill=255)
    canvas.putalpha(mask)
    buf = io.BytesIO()
    canvas.save(buf, "PNG")
    with open(f"{OUT}/m6_png_scaled_masked.png", "wb") as f:
        f.write(buf.getvalue())
    print(f"✓ Method 6: PNG scaled+masked → m6_png_scaled_masked.png (scaled {img.size}→{scaled.size})")
except Exception as e:
    print(f"✗ Method 6: PNG scaled+masked → {e}")

print("\nDone. Compare the m1-m6 files in assets/testing/.")
