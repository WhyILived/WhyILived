"""
Download and standardize shield.io badges, then generate the pyramid SVG
with base64-embedded badges (required for GitHub rendering).

Usage:
    python scripts/download_badges.py

Config: edit BADGES list below. Output:
    - assets/badges/ directory with standardized 96×28 PNG badges (AR preserved, padded)
    - assets/stack-pyramid.svg rebuilt with base64-embedded badges
"""

import base64
import io
import os
import sys

import requests
from PIL import Image, ImageDraw

# ─── Configuration ─────────────────────────────────────────────
TARGET_WIDTH = 96
TARGET_HEIGHT = 28
OUTPUT_DIR = "assets/badges"
SVG_PATH = "assets/stack-pyramid.svg"

# Pyramid geometry — block width=96, no gaps, centered at x=450
# start_x = 450 - (n * 96) / 2
# Row positions (y from top, grounded at y=380)
# Block height=28, no vertical gaps
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

# Which rows need fillers (indices into ROW_X)
FILLER_ROWS = {2, 3, 5, 6}


def shields_url(label: str, color: str, logo: str, style: str = "for-the-badge") -> str:
    """Build a shields.io badge URL (PNG for PIL processing)."""
    url = f"https://img.shields.io/badge/{label}-{color}.png"
    params = [f"style={style}"]
    if logo:
        params.append(f"logo={logo}")
        params.append("logoColor=white")
    return url + "?" + "&".join(params)


def download_badge(url: str, filepath: str, bg_color: str, target_w: int, target_h: int, corner_rx: int = 5) -> bool:
    """Download PNG badge, scale with LANCZOS, center on canvas, apply rounded corners."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGBA")

        # Scale to fit within target while preserving aspect ratio
        w_ratio = target_w / img.width
        h_ratio = target_h / img.height
        scale = min(w_ratio, h_ratio)
        new_w = max(1, int(img.width * scale))
        new_h = max(1, int(img.height * scale))
        scaled = img.resize((new_w, new_h), Image.LANCZOS)

        # Create canvas with badge background color
        canvas = Image.new("RGBA", (target_w, target_h), (*bytes.fromhex(bg_color), 255))

        # Paste badge centered
        px = (target_w - new_w) // 2
        py = (target_h - new_h) // 2
        canvas.paste(scaled, (px, py), scaled)

        # Apply rounded-rect mask
        mask = Image.new("L", (target_w, target_h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), (target_w - 1, target_h - 1)],
            radius=corner_rx,
            fill=255,
        )
        canvas.putalpha(mask)
        canvas.save(filepath, "PNG")
        print(f"  ✓ {filepath} ({img.width}x{img.height} → {scaled.width}x{scaled.height})")
        return True
    except Exception as e:
        print(f"  ✗ {filepath}: {e}")
        return False


def badge_base64(filepath: str) -> str:
    """Read a PNG file and return a base64 data URI string."""
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def read_existing_svg(path: str) -> str:
    """Read the existing SVG, preserving everything before and after the pyramid."""
    with open(path, "r") as f:
        return f.read()


def generate_pyramid_svg(existing_svg: str) -> str:
    """Replace the pyramid section with base64-embedded badges."""
    # Find the pyramid comment block
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
    lines.append("       PYRAMID — 7 rows, blocks touch (96×28 shields.io)")
    lines.append("       Filler blocks: 96×28 dark rect (#21262d, rx=5)")
    lines.append("       Row 7 bottom touches y=380")
    lines.append("       ══════════════════════════════════════════════════ -->")
    lines.append("")

    badge_idx = 0
    filler_rows_done = {2: 0, 5: 0, 6: 0}

    # Render rows 7 → 1 (bottom to top)
    for row_num in range(7, 0, -1):
        y = ROW_Y[7 - row_num]
        positions = ROW_X[row_num]
        filler_count = len(positions) - min(len(positions), len(BADGES) - badge_idx)

        # Determine how many real badges vs fillers for this row
        row_badge_count = len(positions)
        if row_num in FILLER_ROWS:
            if row_num == 2:
                row_badge_count = 2  # Docker, K8s
            elif row_num == 3:
                row_badge_count = 2  # AWS, GH Actions
            elif row_num == 5:
                row_badge_count = 4  # React, Next, Svelte, Vue
            elif row_num == 6:
                row_badge_count = 4  # Angular, FastAPI, Django, Node

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
                # Real badge
                if badge_idx >= len(BADGES):
                    print(f"ERROR: Not enough badges defined for row {row_num}")
                    sys.exit(1)
                label_url, color, logo = BADGES[badge_idx]
                filename = label_url.replace("%20", "_").replace("%2B%2B", "plusplus")
                filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")
                b64 = badge_base64(filepath)
                if label_url == "Arch%20Linux":
                    lines.append(f'  <image class="apex-badge" x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" href="{b64}" filter="url(#apex-glow)"/>')
                else:
                    lines.append(f'  <image x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" href="{b64}"/>')
                badge_idx += 1
            else:
                # Filler block
                lines.append(f'  <rect x="{x}" y="{y}" width="{TARGET_WIDTH}" height="{TARGET_HEIGHT}" rx="5" fill="#21262d"/>')

        lines.append("")

    pyramid_section = "\n".join(lines)
    return header + pyramid_section + footer


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Downloading {len(BADGES)} badges to {OUTPUT_DIR}/")
    print(f"Target size: {TARGET_WIDTH}×{TARGET_HEIGHT} (PNG source, LANCZOS scale)\n")

    success = 0
    for label, color, logo in BADGES:
        url = shields_url(label, color, logo)
        filename = label.replace("%20", "_").replace("%2B%2B", "plusplus")
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")
        if download_badge(url, filepath, color, TARGET_WIDTH, TARGET_HEIGHT):
            success += 1

    print(f"\n{success}/{len(BADGES)} badges downloaded.\n")

    if success == len(BADGES):
        # Rebuild the pyramid SVG with base64-embedded badges
        existing = read_existing_svg(SVG_PATH)
        new_svg = generate_pyramid_svg(existing)
        with open(SVG_PATH, "w") as f:
            f.write(new_svg)
        print(f"✓ {SVG_PATH} rebuilt with base64-embedded badges.")
    else:
        print("✗ Some badges failed to download. Not rebuilding SVG.")


if __name__ == "__main__":
    main()
