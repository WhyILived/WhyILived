"""
Test: inline SVG badges with AR-preserving scale + brand-color background fill.
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

w_match = re.search(r'width="([0-9.]+)"', svg_raw)
h_match = re.search(r'height="([0-9.]+)"', svg_raw)
orig_w = float(w_match.group(1))
orig_h = float(h_match.group(1))

# Strip outer svg tags
inner = svg_raw[svg_raw.find(">") + 1:]
if inner.rstrip().endswith("</svg>"):
    inner = inner.rstrip()[:-len("</svg>")]

# Calculate AR-preserving scale and centering
scale = min(TARGET_W / orig_w, TARGET_H / orig_h)
scaled_w = orig_w * scale
scaled_h = orig_h * scale
offset_x = (TARGET_W - scaled_w) / 2
offset_y = (TARGET_H - scaled_h) / 2

bg_color = "3178C6"

print(f"Original: {orig_w}x{orig_h}")
print(f"Scale: {scale:.6f}")
print(f"Scaled size: {scaled_w:.2f}x{scaled_h:.2f}")
print(f"Offset: ({offset_x:.2f}, {offset_y:.2f})")

# Stage 1: Raw SVG
with open(f"{OUT}/01_raw.svg", "w") as f:
    f.write(svg_raw)
print(f"\n✓ 01_raw.svg")

# Stage 2: Background rect + scaled inline content
svg_with_bg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
svg_with_bg += f'  <rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="5" fill="#{bg_color}"/>\n'
svg_with_bg += f'  <g transform="translate({offset_x:.4f}, {offset_y:.4f}) scale({scale:.6f})">\n'
svg_with_bg += inner
svg_with_bg += "\n  </g>\n</svg>"
with open(f"{OUT}/02_bg_scaled.svg", "w") as f:
    f.write(svg_with_bg)
print(f"✓ 02_bg_scaled.svg (96x28 bg rect + AR-scaled content)")

# Stage 3: Base64 version for embedding in <image>
b64 = base64.b64encode(svg_with_bg.encode()).decode()
data_uri = f"data:image/svg+xml;base64,{b64}"
test_embed = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}">\n'
test_embed += f'  <image width="{TARGET_W}" height="{TARGET_H}" href="{data_uri}"/>\n'
test_embed += "</svg>"
with open(f"{OUT}/03_embedded_base64.svg", "w") as f:
    f.write(test_embed)
print(f"✓ 03_embedded_base64.svg (base64 SVG in <image>)")

# Also test with a narrow badge (C at 52px) to show scaling up behavior
url_c = "https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=c&logoColor=white"
resp_c = requests.get(url_c, timeout=10, headers={"Accept": "image/svg+xml"})
svg_c = resp_c.content.decode()
w_c = float(re.search(r'width="([0-9.]+)"', svg_c).group(1))
h_c = float(re.search(r'height="([0-9.]+)"', svg_c).group(1))
inner_c = svg_c[svg_c.find(">") + 1:]
if inner_c.rstrip().endswith("</svg>"):
    inner_c = inner_c.rstrip()[:-len("</svg>")]
scale_c = min(TARGET_W / w_c, TARGET_H / h_c)
ox_c = (TARGET_W - w_c * scale_c) / 2
oy_c = (TARGET_H - h_c * scale_c) / 2
bg_c = "A8B9CC"
svg_c_final = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
svg_c_final += f'  <rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="5" fill="#{bg_c}"/>\n'
svg_c_final += f'  <g transform="translate({ox_c:.4f}, {oy_c:.4f}) scale({scale_c:.6f})">\n'
svg_c_final += inner_c
svg_c_final += "\n  </g>\n</svg>"
with open(f"{OUT}/04_c_bg_scaled.svg", "w") as f:
    f.write(svg_c_final)
print(f"✓ 04_c_bg_scaled.svg (C badge: {w_c}px → scaled to fit 96x28, bg fills remainder)")

print(f"\n--- Compare ---")
print(f"02_bg_scaled.svg       - TypeScript: AR-scaled on 96x28 bg")
print(f"03_embedded_base64.svg - Same but as base64 <image>")
print(f"04_c_bg_scaled.svg     - C (narrow badge): AR-scaled on 96x28 bg")
print(f"\nTypeScript scales DOWN (126.5→96). C scales UP (52→96). Both maintain AR.")
