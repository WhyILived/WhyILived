"""
Download shield.io SVG badges and embed them in the pyramid SVG.

Each badge is fetched as SVG, scaled to fit 96x28 while preserving aspect
ratio, placed on a brand-colored rounded-rect background, and embedded
as a base64 SVG data URI in the pyramid SVG (required for GitHub CSP).

Usage:
    python scripts/download_badges.py

Config: edit BADGES list below. Output:
    - assets/badges/ directory with standardized 96x28 SVG badges
    - assets/stack-pyramid.svg rebuilt with base64-embedded badges
"""

import base64
import os
import re
import sys

import requests

# ─── Configuration ─────────────────────────────────────────────
TARGET_WIDTH = 96
TARGET_HEIGHT = 28
CORNER_RX = 5
OUTPUT_DIR = "assets/badges"
SVG_PATH = "assets/stack-pyramid.svg"

# Pyramid geometry — block width=96, no gaps, centered at x=450
ROW_Y = [352, 324, 296, 268, 240, 212, 184]  # rows 7→1 (bottom to top)
ROW_X = {
    1: [402],
    2: [354, 450],
    3: [306, 402, 498],
    4: [258, 354, 450, 546],
    5: [210, 306, 402, 498, 594],
    6: [162, 258, 354, 450, 546, 642],
    7: [114, 210, 306, 402, 498, 594, 690],
}

# Each badge: (label_for_url, color_hex, logo_slug)
BADGES = [
    # Row 7 — Languages (7)
    ("TypeScript", "3178C6", "typescript"),
    ("C%2B%2B", "00599C", "cplusplus"),
    ("Python", "3776AB", "python"),
    ("Rust", "CE422B", "rust"),
    ("C", "A8B9CC", "c"),
    ("Lua", "000080", "lua"),
    ("Java", "ED8B00", "openjdk"),
    # Row 6 — Frameworks cont. (4 real + 2 fillers)
    ("Angular", "DD0031", "angular"),
    ("FastAPI", "009688", "fastapi"),
    ("Django", "092E20", "django"),
    ("Node.js", "339933", "nodejs"),
    # Row 5 — Frameworks (4 real + 1 filler)
    ("React", "61DAFB", "react"),
    ("Next.js", "000000", "nextdotjs"),
    ("Svelte", "FF3E00", "svelte"),
    ("Vue.js", "4FC08D", "vuedotjs"),
    # Row 4 — Databases (4)
    ("PostgreSQL", "4169E1", "postgresql"),
    ("MySQL", "F29111", "mysql"),
    ("Redis", "DC382D", "redis"),
    ("SQLite", "003B57", "sqlite"),
    # Row 3 — DevOps cont. (2 real + 1 filler)
    ("AWS", "FF9900", "amazonaws"),
    ("GitHub%20Actions", "2088FF", "githubactions"),
    # Row 2 — DevOps (2)
    ("Docker", "2496ED", "docker"),
    ("Kubernetes", "326CE5", "kubernetes"),
    # Row 1 — Apex (1)
    ("Arch%20Linux", "1793D1", "archlinux"),
]

# Which rows need fillers
FILLER_ROWS = {2, 3, 5, 6}


def shields_url(label: str, color: str, logo: str, style: str = "for-the-badge") -> str:
    """Build a shields.io badge URL (SVG for sharp rendering)."""
    url = f"https://img.shields.io/badge/{label}-{color}.svg"
    params = [f"style={style}"]
    if logo:
        params.append(f"logo={logo}")
        params.append("logoColor=white")
    return url + "?" + "&".join(params)


def fetch_svg(url: str) -> str:
    """Download SVG from shields.io and return the raw string."""
    resp = requests.get(url, timeout=10, headers={"Accept": "image/svg+xml"})
    resp.raise_for_status()
    return resp.text


def extract_inner(svg_text: str) -> tuple[float, float, str]:
    """Extract width, height, and inner content from a shields.io SVG."""
    w_match = re.search(r'width="([0-9.]+)"', svg_text)
    h_match = re.search(r'height="([0-9.]+)"', svg_text)
    orig_w = float(w_match.group(1))
    orig_h = float(h_match.group(1))
    inner = svg_text[svg_text.find(">") + 1:]
    if inner.rstrip().endswith("</svg>"):
        inner = inner.rstrip()[:-len("</svg>")]
    return orig_w, orig_h, inner


def build_badge_svg(inner: str, orig_w: float, orig_h: float, bg_color: str,
                    target_w: int, target_h: int, corner_rx: int) -> str:
    """Build a 96x28 SVG with brand-color background, AR-scaled badge, and clipPath."""
    scale = min(target_w / orig_w, target_h / orig_h)
    offset_x = (target_w - orig_w * scale) / 2
    offset_y = (target_h - orig_h * scale) / 2

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{target_w}" height="{target_h}" viewBox="0 0 {target_w} {target_h}">\n'
    svg += f'  <defs><clipPath id="clip"><rect x="0" y="0" width="{target_w}" height="{target_h}" rx="{corner_rx}"/></clipPath></defs>\n'
    svg += f'  <rect x="0" y="0" width="{target_w}" height="{target_h}" rx="{corner_rx}" fill="#{bg_color}"/>\n'
    svg += f'  <g clip-path="url(#clip)">\n'
    svg += f'    <g transform="translate({offset_x:.4f}, {offset_y:.4f}) scale({scale:.6f})">\n'
    svg += inner
    svg += "\n    </g>\n"
    svg += "  </g>\n</svg>"
    return svg


def badge_svg_to_base64(svg_text: str) -> str:
    """Encode SVG as base64 data URI."""
    b64 = base64.b64encode(svg_text.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"


def download_badge(url: str, filepath: str, bg_color: str,
                   target_w: int, target_h: int, corner_rx: int) -> bool:
    """Download SVG badge, scale AR, add bg + clipPath, save as .svg."""
    try:
        svg_raw = fetch_svg(url)
        orig_w, orig_h, inner = extract_inner(svg_raw)
        badge_svg = build_badge_svg(inner, orig_w, orig_h, bg_color, target_w, target_h, corner_rx)
        with open(filepath, "w") as f:
            f.write(badge_svg)
        scale = min(target_w / orig_w, target_h / orig_h)
        print(f"  ✓ {filepath} ({orig_w}x{orig_h} → scale {scale:.4f})")
        return True
    except Exception as e:
        print(f"  ✗ {filepath}: {e}")
        return False


def badge_base64(filepath: str) -> str:
    """Read an SVG file and return a base64 data URI string."""
    with open(filepath, "r") as f:
        data = base64.b64encode(f.read().encode()).decode()
    return f"data:image/svg+xml;base64,{data}"


def read_existing_svg(path: str) -> str:
    """Read the existing SVG, preserving everything before and after the pyramid."""
    with open(path, "r") as f:
        return f.read()


def generate_pyramid_svg(existing_svg: str) -> str:
    """Replace the pyramid section with base64-embedded SVG badges."""
    start_marker = "  <!-- ══════════════════════════════════════════════════\n       PYRAMID"
    end_marker = "</svg>"

    start_idx = existing_svg.find(start_marker)
    end_idx = existing_svg.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find pyramid section in SVG")
        sys.exit(1)

    header = existing_svg[:start_idx]
    footer = existing_svg[end_idx:]

    lines = []
    lines.append("  <!-- ══════════════════════════════════════════════════")
    lines.append("       PYRAMID — 7 rows, blocks touch (96×28 SVG badges)")
    lines.append("       Filler blocks: 96×28 dark rect (#21262d, rx=5)")
    lines.append("       Row 7 bottom touches y=380")
    lines.append("       ══════════════════════════════════════════════════ -->")
    lines.append("")

    badge_idx = 0

    for row_num in range(7, 0, -1):
        y = ROW_Y[7 - row_num]
        positions = ROW_X[row_num]

        row_badge_count = len(positions)
        if row_num in FILLER_ROWS:
            if row_num == 2:
                row_badge_count = 2
            elif row_num == 3:
                row_badge_count = 2
            elif row_num == 5:
                row_badge_count = 4
            elif row_num == 6:
                row_badge_count = 4

        label = f"Row {row_num}"
        if row_num == 1:
            label = "Row 1 — Apex: Arch Linux"
        elif row_num == 2:
            label = "Row 2 — DevOps"
        elif row_num == 3:
            label = "Row 3 — DevOps cont."
        elif row_num == 4:
            label = "Row 4 — Databases"
        elif row_num == 5:
            label = "Row 5 — Frameworks"
        elif row_num == 6:
            label = "Row 6 — Frameworks cont."
        elif row_num == 7:
            label = "Row 7 — Languages"

        x_str = ", ".join(str(x) for x in positions)
        lines.append(f"  <!-- {label} ({row_badge_count} blocks + {len(positions) - row_badge_count} filler(s), y={y}) -->")
        lines.append(f"  <!-- x: {x_str} -->")

        for i, x in enumerate(positions):
            if i < row_badge_count:
                if badge_idx >= len(BADGES):
                    print(f"ERROR: Not enough badges defined for row {row_num}")
                    sys.exit(1)
                label_url, color, logo = BADGES[badge_idx]
                filename = label_url.replace("%20", "_").replace("%2B%2B", "plusplus")
                filepath = os.path.join(OUTPUT_DIR, f"{filename}.svg")
                b64 = badge_base64(filepath)
                if label_url == "Arch%20Linux":
                    lines.append(f'  <image class="apex-badge" x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" href="{b64}" filter="url(#apex-glow)"/>')
                else:
                    lines.append(f'  <image x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" href="{b64}"/>')
                badge_idx += 1
            else:
                lines.append(f'  <rect x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" rx="5" fill="#21262d"/>')

        lines.append("")

    pyramid_section = "\n".join(lines)
    return header + pyramid_section + footer


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Downloading {len(BADGES)} badges to {OUTPUT_DIR}/")
    print(f"Target size: {TARGET_WIDTH}x{TARGET_HEIGHT} (SVG source, AR-preserving scale)\n")

    success = 0
    for label, color, logo in BADGES:
        url = shields_url(label, color, logo)
        filename = label.replace("%20", "_").replace("%2B%2B", "plusplus")
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.svg")
        if download_badge(url, filepath, color, TARGET_WIDTH, TARGET_HEIGHT, CORNER_RX):
            success += 1

    print(f"\n{success}/{len(BADGES)} badges downloaded.\n")

    if success == len(BADGES):
        existing = read_existing_svg(SVG_PATH)
        new_svg = generate_pyramid_svg(existing)
        with open(SVG_PATH, "w") as f:
            f.write(new_svg)
        print(f"✓ {SVG_PATH} rebuilt with base64-embedded SVG badges.")
    else:
        print("✗ Some badges failed to download. Not rebuilding SVG.")


if __name__ == "__main__":
    main()
