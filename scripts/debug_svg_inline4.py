"""
Test: inline SVG with AR-preserving scale + clipPath for rounded corners.
"""

import base64
import os
import re

import requests

URL = "https://img.shields.io/badge/TypeScript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white"
TARGET_W = 96
TARGET_H = 28
RX = 5
OUT = "assets/testing"
os.makedirs(OUT, exist_ok=True)

resp = requests.get(URL, timeout=10, headers={"Accept": "image/svg+xml"})
svg_raw = resp.content.decode()

w_match = re.search(r'width="([0-9.]+)"', svg_raw)
h_match = re.search(r'height="([0-9.]+)"', svg_raw)
orig_w = float(w_match.group(1))
orig_h = float(h_match.group(1))

inner = svg_raw[svg_raw.find(">") + 1:]
if inner.rstrip().endswith("</svg>"):
    inner = inner.rstrip()[:-len("</svg>")]

scale = min(TARGET_W / orig_w, TARGET_H / orig_h)
scaled_w = orig_w * scale
scaled_h = orig_h * scale
offset_x = (TARGET_W - scaled_w) / 2
offset_y = (TARGET_H - scaled_h) / 2

bg_color = "3178C6"
print(f"Original: {orig_w}x{orig_h}, scale={scale:.6f}")
print(f"Scaled: {scaled_w:.2f}x{scaled_h:.2f}, offset=({offset_x:.2f}, {offset_y:.2f})")

# Stage 1: Raw SVG
with open(f"{OUT}/01_raw.svg", "w") as f:
    f.write(svg_raw)
print(f"\n✓ 01_raw.svg")

# Stage 2: Background + clipPath + scaled content
svg_clipped = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
svg_clipped += f'  <defs>\n'
svg_clipped += f'    <clipPath id="badge-clip"><rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="{RX}"/></clipPath>\n'
svg_clipped += f'  </defs>\n'
svg_clipped += f'  <rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="{RX}" fill="#{bg_color}"/>\n'
svg_clipped += f'  <g clip-path="url(#badge-clip)">\n'
svg_clipped += f'    <g transform="translate({offset_x:.4f}, {offset_y:.4f}) scale({scale:.6f})">\n'
svg_clipped += inner
svg_clipped += "\n    </g>\n"
svg_clipped += f"  </g>\n</svg>"
with open(f"{OUT}/02_clipped.svg", "w") as f:
    f.write(svg_clipped)
print(f"✓ 02_clipped.svg (background rect + clipPath + scaled content)")

# Stage 3: Base64 embed version
b64 = base64.b64encode(svg_clipped.encode()).decode()
data_uri = f"data:image/svg+xml;base64,{b64}"
test_embed = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}">\n'
test_embed += f'  <image width="{TARGET_W}" height="{TARGET_H}" href="{data_uri}"/>\n'
test_embed += "</svg>"
with open(f"{OUT}/03_embedded.svg", "w") as f:
    f.write(test_embed)
print(f"✓ 03_embedded.svg (base64 in <image>)")

# Stage 4: C badge (narrow) with clipping
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
svg_c_clipped = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TARGET_W}" height="{TARGET_H}" viewBox="0 0 {TARGET_W} {TARGET_H}">\n'
svg_c_clipped += f'  <defs><clipPath id="c-clip"><rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="{RX}"/></clipPath></defs>\n'
svg_c_clipped += f'  <rect x="0" y="0" width="{TARGET_W}" height="{TARGET_H}" rx="{RX}" fill="#{bg_c}"/>\n'
svg_c_clipped += f'  <g clip-path="url(#c-clip)"><g transform="translate({ox_c:.4f}, {oy_c:.4f}) scale({scale_c:.6f})">\n'
svg_c_clipped += inner_c + "\n  </g></g>\n</svg>"
with open(f"{OUT}/04_c_clipped.svg", "w") as f:
    f.write(svg_c_clipped)
print(f"✓ 04_c_clipped.svg (C badge, AR-scaled + clipped)")

print(f"\n--- Compare ---")
print(f"02_clipped.svg  - TypeScript with clipPath (should fix sharp corners)")
print(f"03_embedded.svg - Same as base64 <image>")
print(f"04_c_clipped.svg - C badge (narrow) with clipPath")
