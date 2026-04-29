"""
Test: inline SVG badges using string manipulation instead of xml.etree.ElementTree.
"""

import base64
import os
import re

import requests

URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
TARGET_W = 96
TARGET_H = 28
OUT = "assets/testing"
os.makedirs(OUT, exist_ok=True)

# Fetch raw SVG
resp = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
svg_raw = resp.content.decode()

# Extract width and height from the root SVG tag
w_match = re.search(r'width="([0-9.]+)"', svg_raw)
h_match = re.search(r'height="([0-9.]+)"', svg_raw)
orig_w = float(w_match.group(1))
orig_h = float(h_match.group(1))

sx = TARGET_W / orig_w
sy = TARGET_H / orig_h
print(f"Original: {orig_w}x{orig_h}, scale: x={sx:.6f}, y={sy:.6f}")

# Strip the outer <svg ...> and </svg> tags to get inner content
# The SVG always starts with <svg ...> and ends with </svg>
inner = svg_raw[svg_raw.find(">") + 1:]  # everything after first >
if inner.rstrip().endswith("</svg>"):
    inner = inner.rstrip()[:-len("</svg>")]

print(f"Inner content: {len(inner)} chars")

# Stage 1: Raw SVG
with open(f"{OUT}/01_raw.svg", "w") as f:
    f.write(svg_raw)
print(f"✓ 01_raw.svg")

# Stage 2: Inline direct (string-based, no ET)
inline_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
inline_svg += f'  <g transform="scale({sx}, {sy})">\n'
inline_svg += inner
inline_svg += "\n  </g>\n</svg>"
with open(f"{OUT}/02_inline_string.svg", "w") as f:
    f.write(inline_svg)
print(f"✓ 02_inline_string.svg (string-based, no ET mangling)")

# Stage 3: Inline with viewBox only (no width/height)
inline_svg_vb = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
inline_svg_vb += f'  <g transform="scale({sx}, {sy})">\n'
inline_svg_vb += inner
inline_svg_vb += "\n  </g>\n</svg>"
with open(f"{OUT}/03_viewbox_only.svg", "w") as f:
    f.write(inline_svg_vb)
print(f"✓ 03_viewbox_only.svg")

# Stage 4: Inline with width/height only (no viewBox)
inline_svg_wh = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}">\n'
inline_svg_wh += f'  <g transform="scale({sx}, {sy})">\n'
inline_svg_wh += inner
inline_svg_wh += "\n  </g>\n</svg>"
with open(f"{OUT}/04_size_only.svg", "w") as f:
    f.write(inline_svg_wh)
print(f"✓ 04_size_only.svg")

# Stage 5: Base64 SVG data URI in <image>
svg_b64 = base64.b64encode(inline_svg.encode()).decode()
data_uri = f"data:image/svg+xml;base64,{svg_b64}"
test_embed = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}">\n'
test_embed += f'  <image width="{TARGET_W}" height="{TARGET_H}" href="{data_uri}"/>\n'
test_embed += "</svg>"
with open(f"{OUT}/05_embedded_base64.svg", "w") as f:
    f.write(test_embed)
print(f"✓ 05_embedded_base64.svg")

# Stage 6: Compare with rasterized
try:
    import cairosvg
    png = cairosvg.svg2png(bytestring=svg_raw.encode(), output_width=TARGET_W, output_height=TARGET_H)
    with open(f"{OUT}/06_cairo_png.png", "wb") as f:
        f.write(png)
    print(f"✓ 06_cairo_png.png")
except Exception as e:
    print(f"✗ 06: {e}")

print(f"\n--- Compare in your viewer ---")
print(f"02_inline_string.svg   - 96x28 + viewBox + scale (string-based)")
print(f"03_viewbox_only.svg    - viewBox only (no fixed dimensions)")
print(f"04_size_only.svg       - width/height only (no viewBox)")
print(f"05_embedded_base64.svg - base64 SVG in <image>")
print(f"06_cairo_png.png       - rasterized (blurry reference)")
