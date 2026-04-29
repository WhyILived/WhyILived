# Tech Stack Pyramid — Design Document

## Overview

Replace the current tech stack badge rows in `README.md` with a **custom SVG pyramid** — 7 rows of blocks, each row naturally 1 block wider than the one above it (1, 2, 3, 4, 5, 6, 7 = 28 total slots). Categories span 1 or more rows.

**Context:** The README already has a space/starry/orbital theme. The pyramid should be a native SVG asset with a matching starry background.

---

## Pyramid Geometry

7 rows, each row `r` (1-indexed from top) has `r` blocks:

| Row | Blocks | Total so far |
|-----|--------|-------------|
| 1   | 1      | 1           |
| 2   | 2      | 3           |
| 3   | 3      | 6           |
| 4   | 4      | 10          |
| 5   | 5      | 15          |
| 6   | 6      | 21          |
| 7   | 7      | **28**      |

24 real items + **4 filler blocks** = 28 slots exactly.

---

## Tech Stack Items — 7-Row Structure

### Row 1 — Linux (1 block, 0 fillers)
- **Arch Linux** — apex, prominent orange block

### Rows 2-3 — DevOps & Infra (5 blocks, 1 filler in row 3)

**Row 2** — Docker, Kubernetes

**Row 3** — AWS, GitHub Actions, [filler]

### Row 4 — Databases (4 blocks, 0 fillers)
- PostgreSQL
- MySQL
- Redis
- SQLite

### Rows 5-6 — Frameworks (9 blocks, 3 fillers across rows 5 and 6)

**Row 5** — React, Next.js, Svelte, Vue, [filler]

**Row 6** — Angular, FastAPI, Django, Node.js, [filler], [filler]

### Row 7 — Languages (7 blocks, 0 fillers)
- TypeScript
- C++
- Python
- Rust
- C
- Lua
- Java

---

## Block Layout Per Row

Each row is horizontally centered. Blocks sit flush with no gaps — every block in a row is the same size, evenly spaced across the row width.

**Row 7** (7 blocks): TypeScript · C++ · Python · Rust · C · Lua · Java
**Row 6** (6 blocks): Angular · FastAPI · Django · Node.js · [filler] · [filler]
**Row 5** (5 blocks): React · Next.js · Svelte · Vue · [filler]
**Row 4** (4 blocks): PostgreSQL · MySQL · Redis · SQLite
**Row 3** (3 blocks): AWS · GitHub Actions · [filler]
**Row 2** (2 blocks): Docker · Kubernetes
**Row 1** (1 block): Arch Linux

---

## Design Direction

### Layout
- Downward-pointing pyramid: apex at top (Arch Linux), naturally widening downward
- Each row has `r` blocks — no gaps within a row
- Rows are visually distinct but flow into each other
- No space between adjacent blocks — blocks touch, forming a solid pyramid face

### Visual Style
- **Starfield background** matching `orbital.svg` / `header.svg` aesthetic (`#0d1117` background, small twinkling star circles)
- **Badge blocks** — each item is a rounded rect (rx=5), filled with the brand color, centered text label in contrasting color
- **Category labels** — bracket/marker lines on the right side of the pyramid, pointing to the relevant rows
- **Filler blocks** — same shape/size as real blocks, neutral dark fill (#21262d), no text
- **Arch Linux apex** — uses orange (#F99E3A) matching the header title color

### Bracket Labels
- Category labels sit on the **right side** of the pyramid, outside the block area
- A vertical bracket arm runs along the right edge
- Horizontal lines connect bracket to relevant rows
- Labels: 🐧 Linux, 🚀 DevOps & Infra, 🗄️ Databases, 🛠️ Frameworks, 💻 Languages

### Color Palette
| Element | Color |
|---|---|
| Background | `#0d1117` |
| Accent / Header orange | `#F99E3A` |
| Star blue | `#58a6ff` |
| Star amber | `#e6b450` |
| Text / Labels | `#c9d1d9` |
| Bracket lines | `#30363d` |
| Filler blocks | `#21262d` |

---

## Block Width Calculation

All rows share the same overall width (fills 900px viewBox). Block width is chosen so the **bottom row (7 blocks) fits perfectly** with no overflow and a small margin.

For Row 7 (7 blocks, no gaps):
- Available width: ~860px (40px margin each side)
- Block width + spacing = 860 / 7 ≈ 123px per block slot
- Let block width = 110px, gap = 13px → 7×110 + 6×13 = 770 + 78 = 848px ✓

Each row above is centered, so Row 6 (6 blocks) uses the same block width:
- 6×110 + 5×13 = 660 + 65 = 725px → centered at x=450 → x starts at ~(900-725)/2 = 87.5

Proceed similarly for all rows.

---

## Category Label Layout

Labels on the right side (x > rightmost block), vertically spanning their rows:

| Category | Rows | Bracket x |
|---|---|---|
| 💻 Languages | 7 | ~860 |
| 🛠️ Frameworks | 5-6 | ~860 |
| 🗄️ Databases | 4 | ~860 |
| 🚀 DevOps & Infra | 2-3 | ~860 |
| 🐧 Linux | 1 | ~860 |

Label text at right edge, bracket lines connect to row level.

---

## Files

| File | Role |
|---|---|
| `README.md` | Has `<img src="./assets/stack-pyramid.svg">` for tech stack section |
| `assets/stack-pyramid.svg` | The pyramid SVG — 900×450 viewBox |

---

## Technical Notes

### Badge Rendering
Inline SVG `<rect>` + `<text>` for each block — no external images. Brand colors from shield.io / official logos.

### Animation
- Subtle twinkle on star background (`@keyframes tw-a/b/c` matching `orbital.svg`)
- Optional pulse on Arch Linux apex block

---

## Bugs / TODO

- [ ] Bracket lines for rows 2, 4, 5 pass through badge rects — need bracket to sit on outside of pyramid only (no horizontal line crossing pyramid width), or remove horizontal segment entirely and use just the vertical bracket arm on the right side
- [ ] Implement the 7-row structure — blocks must touch with no gaps
- [ ] Filler blocks: neutral dark fill, no text

---

## Implementation Order

1. Rebuild `assets/stack-pyramid.svg` — 7-row pyramid, blocks flush/touching, correct block widths, filler blocks, bracket labels on right side only
2. Verify in browser — pyramid looks like a solid monument, no gaps between blocks

---

## Reference: Existing Theme SVGs

- `assets/header.svg` — viewBox `900×140`, starfield, `#F99E3A` title, `@keyframes h-tw-*`
- `assets/orbital.svg` — viewBox `900×430`, starfield, animated planets, CSS classes for animations
- Both use `monospace` font, `#0d1117` background

The pyramid SVG should share:
- Background color and star style
- Font (`monospace`)
- Animation keyframes