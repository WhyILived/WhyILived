"""
Test: inline SVG badges instead of rasterizing to PNG.
Approach: scale internal elements to fit 96x28 while keeping everything vector.
"""

import base64
import io
import os
import xml.etree.ElementTree as ET

import requests

URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
TARGET_W = 96
TARGET_H = 28
OUT = "assets/testing"
os.makedirs(OUT, exist_ok=True)

# Stage 1: Raw SVG
resp = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
svg_raw = resp.content
with open(f"{OUT}/01_raw.svg", "wb") as f:
    f.write(svg_raw)
print(f"✓ Stage 1: raw SVG → 01_raw.svg")

# Parse the SVG
ns = {"svg": "http://www.w3.org/2000/svg"}
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

root = ET.fromstring(svg_raw)
orig_w = float(root.get("width"))
orig_h = float(root.get("height"))
print(f"  Original: {orig_w}x{orig_h}")

sx = TARGET_W / orig_w
sy = TARGET_H / orig_h
print(f"  Scale factors: x={sx:.6f}, y={sy:.6f}")

# Stage 2: Wrap in scaled group
# Create new SVG root
new_root = ET.Element("svg", {
    "xmlns": "http://www.w3.org/2000/svg",
    "width": str(TARGET_W),
    "height": str(TARGET_H),
    "viewBox": f"0 0 {TARGET_W} {TARGET_H}",
})

# Scale group
g = ET.SubElement(new_root, "g", {
    "transform": f"scale({sx:.6f}, {sy:.6f})",
})

# Move all children from original to scaled group
for child in root:
    g.append(child)

# Write transformed SVG
transformed_xml = ET.tostring(new_root, encoding="unicode", xml_declaration=False)
with open(f"{OUT}/02_transformed.svg", "w") as f:
    f.write(transformed_xml)
print(f"✓ Stage 2: transformed SVG → 02_transformed.svg")

# Stage 3: Base64 encode the SVG for embedding
svg_b64 = base64.b64encode(transformed_xml.encode()).decode()
data_uri = f"data:image/svg+xml;base64,{svg_b64}"
with open(f"{OUT}/03_svg_base64.txt", "w") as f:
    f.write(data_uri)
print(f"✓ Stage 3: SVG base64 data URI → 03_svg_base64.txt ({len(data_uri)} chars)")

# Stage 4: Create a test SVG with the embedded badge
test_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}">
  <image x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" href="{data_uri}"/>
</svg>"""
with open(f"{OUT}/04_test_embedded.svg", "w") as f:
    f.write(test_svg)
print(f"✓ Stage 4: test SVG with embedded badge → 04_test_embedded.svg")

# Stage 5: Also test inlining the SVG content directly (no base64)
# This removes the extra image wrapper
inline_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">
  <g transform="scale({sx:.6f}, {sy:.6f})">
"""
for child in root:
    inline_svg += ET.tostring(child, encoding="unicode")
inline_svg += "</g></svg>"
with open(f"{OUT}/05_inline_direct.svg", "w") as f:
    f.write(inline_svg)
print(f"✓ Stage 5: inline direct (no base64 wrapper) → 05_inline_direct.svg")

# Stage 6: Compare with a rasterized version at the same size
try:
    import cairosvg
    png = cairosvg.svg2png(bytestring=svg_raw, output_width=TARGET_W, output_height=TARGET_H)
    with open(f"{OUT}/06_cairo_png.png", "wb") as f:
        f.write(png)
    print(f"✓ Stage 6: cairosvg rasterized (for comparison) → 06_cairo_png.png")
except Exception as e:
    print(f"✗ Stage 6: cairosvg failed → {e}")

print(f"\n--- Compare in your viewer ---")
print(f"01_raw.svg          - Original (will be wrong size in pyramid)")
print(f"02_transformed.svg  - Scaled to 96x28 via transform (vector, should be sharp)")
print(f"03_svg_base64.txt   - Base64 data URI for embedding")
print(f"04_test_embedded.svg - 96x28 container with base64 SVG badge")
print(f"05_inline_direct.svg - 96x28 SVG with inlined content (no base64)")
print(f"06_cairo_png.png    - Rasterized (blurry reference)")
print(f"\nOpen 04_test_embedded.svg or 05_inline_direct.svg to check sharpness!")
