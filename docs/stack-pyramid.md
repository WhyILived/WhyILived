# Tech Stack Pyramid — Design Document

## Overview

Replace the current tech stack badge rows in `README.md` with a **custom SVG pyramid** that displays all tech stack items as visual blocks, arranged in a pyramid shape with category labels.

**Context:** The README already has a space/starry/orbital theme. The pyramid should be a native SVG asset with a matching starry background.

---

## Tech Stack Items

### Row 1 — Apex (1 item)
- **Arch Linux** — single block at the top, styled as a prominent apex element (arch logo or badge)

### Row 2 — DevOps & Infra (4 items)
- Docker
- Kubernetes
- AWS
- GitHub Actions

### Row 3 — Databases (4 items)
- PostgreSQL
- MySQL
- Redis
- SQLite

### Row 4 — Frameworks (8 items)
- React
- Next.js
- Svelte
- Angular
- Vue
- FastAPI
- Django
- Node.js

### Row 5 — Languages (7 items)
- TypeScript
- C++
- Python
- Rust
- C
- Lua
- Java

---

## Design Direction

### Layout
- Downward-pointing pyramid: apex at top (Arch Linux), widening downward
- Each category occupies one row
- Row widths get progressively wider toward the bottom
- Items within each row are evenly spaced

### Visual Style
- **Starfield background** matching the `orbital.svg` / `header.svg` aesthetic (`#0d1117` background, small twinkling star circles)
- **Badge blocks** — each item is a rounded rect pill (using shield.io badge imagery rendered as SVG shapes, or inline SVG badges clipped to rounded rects)
- **Category labels** — positioned with bracket/marker lines on the right side of each row, like:

```
      [Arch Linux]                    ---|
  [Docker] [K8s] [AWS] [GH Actions]   |--- 🚀 DevOps & Infra
[Postgres] [MySQL] [Redis] [SQLite]    ---| 🗄️ Databases
[React] [Next.js] [Svelte]...              |--- 🛠️ Frameworks
[TypeScript] [C++] [Python]...              |--- 💻 Languages
```

- **Bracket lines** — thin lines connecting category labels to their rows, right-aligned
- Arch Linux apex uses **orange (#F99E3A)** matching the header title color

### Pyramid Centering
- The pyramid should be centered within a `900px` wide viewBox
- Each row is centered, items evenly distributed across row width
- Row spacing: ~60-70px between row centers

### Color Palette (from existing theme)
| Element | Color |
|---|---|
| Background | `#0d1117` |
| Accent / Header orange | `#F99E3A` |
| Star blue | `#58a6ff` |
| Star amber | `#e6b450` |
| Text / Labels | `#c9d1d9` |
| Bracket lines | `#30363d` |

---

## Files

| File | Role |
|---|---|
| `README.md` | Replace the existing badge `<div>` with `<img src="./assets/stack-pyramid.svg">` |
| `assets/stack-pyramid.svg` | New SVG file — the pyramid graphic |

---

## Technical Notes

### Badge Rendering
Since shield.io badges are external images, each badge in the SVG should be either:
1. **Inline SVG shapes** — draw the rounded rect + icon + text directly in the SVG (more complex but fully self-contained)
2. **`<img>` tags referencing shield.io** — simpler, but requires network access to render

**Recommendation:** Use inline SVG shapes for the main items, matching the shield.io badge style (rounded rect background, icon on left, text label).

### Row Widths (rough calculations)
- Row 5 (Languages, 7 items): ~800px wide, items ~100px each
- Row 4 (Frameworks, 8 items): ~800px wide, items ~90px each
- Row 3 (DBs, 4 items): ~480px wide
- Row 2 (DevOps, 4 items): ~480px wide
- Row 1 (Apex): centered, single item

### Animation
- Subtle twinkle animation on the star background (same `@keyframes` as `header.svg`)
- Optional: slight pulse on the Arch Linux apex block

---

## Bugs / TODO

- [ ] Bracket lines for rows 2, 4, 5 pass through badge rects — need bracket to sit on outside of pyramid only (no horizontal line crossing pyramid width), or remove horizontal segment entirely and use just the vertical bracket arm on the right side

---

## Implementation Order

1. Create `assets/stack-pyramid.svg` — build the SVG with starfield background, pyramid layout, badge shapes, and bracket labels
2. Update `README.md` — replace the old badge `<div>` with the new SVG `<img>` reference

---

## Reference: Existing Theme SVGs

- `assets/header.svg` — viewBox `900×140`, starfield, `#F99E3A` title, `@keyframes h-tw-*`
- `assets/orbital.svg` — viewBox `900×430`, starfield, animated planets, CSS classes for animations
- Both use `monospace` font, `#0d1117` background

The pyramid SVG should share the same:
- Background color and star style
- Font (`monospace`)
- Animation keyframes (if any star twinkling is included)
