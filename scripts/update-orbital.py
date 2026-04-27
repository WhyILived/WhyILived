#!/usr/bin/env python3
"""
scripts/update-orbital.py

Fetches the last 12 months of GitHub contribution data for WhyILived and
rewrites the <!-- BEGIN_PLANETS --> ... <!-- END_PLANETS --> section of
assets/orbital.svg with real counts and correctly scaled planet radii.

Usage:
  GITHUB_TOKEN=<token> python3 scripts/update-orbital.py

Run automatically via .github/workflows/update-orbital.yml on the 1st of
each month. Can also be triggered manually from the Actions tab, or run
locally if you have a token with 'read:user' scope.
"""

import json
import math
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from urllib.request import Request, urlopen

# ── Config ─────────────────────────────────────────────────────────────────
USERNAME  = "WhyILived"
SVG_PATH  = "assets/orbital.svg"
API_URL   = "https://api.github.com/graphql"
TOKEN     = os.environ.get("GITHUB_TOKEN", "")
OUTPUT_PATH = None  # None = overwrite SVG_PATH; set via --output for test runs

# Orbit geometry — must match the static SVG template
CX, CY, ORBIT_R = 450, 220, 130
MIN_R, MAX_R     = 3, 12        # planet radius range (pixels)
LABEL_GAP        = 40           # px from planet edge to label anchor

# Month ordering: i=0 = latest/current month, placed at 12-o'clock (-90°).
# Subsequent months go counter-clockwise (subtract 30° per step).
# a_i = -90 - i*30  degrees

COLORS = [
    "#e6b450",  # i=0  latest  (amber)
    "#58a6ff",  # i=1  (bright blue)
    "#9b8cff",  # i=2  (indigo)
    "#39d353",  # i=3  (green)
    "#ff7b72",  # i=4  (coral)
    "#a5d6ff",  # i=5  (pale blue)
    "#ffa657",  # i=6  (orange)
    "#bc8cff",  # i=7  (violet)
    "#79c0ff",  # i=8  (sky blue)
    "#d2a8ff",  # i=9  (purple)
    "#56d364",  # i=10 (lime green)
    "#ffa198",  # i=11 oldest (salmon)
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ── GitHub GraphQL ──────────────────────────────────────────────────────────
QUERY = """
query($username: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $username) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


def gql(query, variables, token):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = Request(API_URL, data=payload, headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "User-Agent": "WhyILived-orbital-updater/1.0",
    })
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


# ── Contribution fetching ───────────────────────────────────────────────────
def fetch_monthly(token):
    """
    Return [(year, month, total_contributions), ...] for the last 12 months,
    ordered latest-first (index 0 = current month).
    """
    now = datetime.now(timezone.utc)

    # Build list of 12 months, oldest first
    months_asc = []
    for offset in range(11, -1, -1):
        m = now.month - offset
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        months_asc.append((y, m))

    from_dt = datetime(months_asc[0][0], months_asc[0][1], 1,
                       tzinfo=timezone.utc)
    to_dt = now

    data = gql(QUERY, {
        "username": USERNAME,
        "from": from_dt.isoformat(),
        "to": to_dt.isoformat(),
    }, token)

    errors = data.get("errors")
    if errors:
        print("GraphQL errors:", errors, file=sys.stderr)
        sys.exit(1)

    counts = {k: 0 for k in months_asc}
    weeks = (data["data"]["user"]
             ["contributionsCollection"]
             ["contributionCalendar"]
             ["weeks"])
    for week in weeks:
        for day in week["contributionDays"]:
            d = datetime.fromisoformat(day["date"])
            key = (d.year, d.month)
            if key in counts:
                counts[key] += day["contributionCount"]

    # Reverse so index 0 = latest month
    return [(y, m, counts[(y, m)]) for y, m in reversed(months_asc)]


# ── Geometry helpers ────────────────────────────────────────────────────────
def planet_pos(i):
    """(px, py) for planet index i. i=0 is at 12-o'clock, CCW ordering."""
    a = math.radians(-90 - i * 30)
    return CX + ORBIT_R * math.cos(a), CY + ORBIT_R * math.sin(a)


def label_pos(i, r):
    """Label anchor: outward from planet centre by (r + LABEL_GAP)."""
    a = math.radians(-90 - i * 30)
    d = r + LABEL_GAP
    px, py = planet_pos(i)
    return px + d * math.cos(a), py + d * math.sin(a)


def scale_radius(count, lo, hi):
    if hi == lo:
        return (MIN_R + MAX_R) // 2
    return round(MIN_R + (count - lo) / (hi - lo) * (MAX_R - MIN_R))


# ── SVG generation ──────────────────────────────────────────────────────────
def build_planets_block(months):
    """
    Build the <g id="sys"> ... </g> content from the months list.
    months: [(year, month, count), ...], index 0 = latest month.
    """
    counts = [c for _, _, c in months]
    lo, hi = min(counts), max(counts)

    lines = ['<g id="sys">']
    for i, (year, month, count) in enumerate(months):
        r     = scale_radius(count, lo, hi)
        color = COLORS[i % len(COLORS)]
        delay = round(i * 0.4, 1)

        px, py = planet_pos(i)
        lx, ly = label_pos(i, r)
        mon    = MONTH_NAMES[month - 1]
        yr_s   = "'{:02d}".format(year % 100)
        label  = "{} {}".format(mon, yr_s)

        lines.append(
            "  <!-- i={i}  {label}  {count}c  r={r}  pos=({px:.0f},{py:.0f})"
            "  label=({lx:.0f},{ly:.0f}) -->".format(
                i=i, label=label, count=count, r=r,
                px=px, py=py, lx=lx, ly=ly,
            )
        )
        lines.append(
            '  <circle class="planet" cx="{px:.0f}" cy="{py:.0f}" r="{r}"'
            ' fill="{color}" filter="url(#glow)"'
            ' style="animation-delay:{delay}s"/>'.format(
                px=px, py=py, r=r, color=color, delay=delay,
            )
        )
        # Vertical offset for label text baseline: centre the text on ly
        ly_text = ly + 3  # small downward nudge so text visually centres on ly
        lines.append(
            '  <text class="planet-text" text-anchor="middle" x="{lx:.0f}" y="{ly:.0f}">'.format(
                lx=lx, ly=ly_text,
            )
        )
        lines.append(
            '    <tspan class="label">{label}</tspan>'
            '<tspan class="label-count" dx="4">{count}</tspan>'.format(
                label=label, count=count,
            )
        )
        lines.append("  </text>")
        lines.append("")

    lines.append("</g>")
    return "\n".join(lines)


# ── SVG update ──────────────────────────────────────────────────────────────
MARKER_RE = re.compile(
    r"<!-- BEGIN_PLANETS -->.*?<!-- END_PLANETS -->",
    re.DOTALL,
)


def update_svg(new_block, output_path=None):
    target = output_path or SVG_PATH
    with open(target, "r", encoding="utf-8") as f:
        svg = f.read()

    if not MARKER_RE.search(svg):
        print(
            "ERROR: BEGIN_PLANETS / END_PLANETS markers not found in",
            target, file=sys.stderr,
        )
        sys.exit(1)

    replacement = (
        "<!-- BEGIN_PLANETS -->\n"
        + new_block
        + "\n<!-- END_PLANETS -->"
    )
    new_svg = MARKER_RE.sub(replacement, svg)

    with open(target, "w", encoding="utf-8") as f:
        f.write(new_svg)

    print("Updated" if not output_path else "Wrote", target)


def write_test_svg(new_block, output_path):
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        svg = f.read()

    if not MARKER_RE.search(svg):
        print(
            "ERROR: BEGIN_PLANETS / END_PLANETS markers not found in",
            SVG_PATH, file=sys.stderr,
        )
        sys.exit(1)

    replacement = (
        "<!-- BEGIN_PLANETS -->\n"
        + new_block
        + "\n<!-- END_PLANETS -->"
    )
    new_svg = MARKER_RE.sub(replacement, svg)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_svg)

    print("Wrote", output_path)


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Update orbital SVG with GitHub contributions.")
    parser.add_argument("--output", "-o", help="Output SVG path (default: overwrite assets/orbital.svg)")
    parser.add_argument("--token", "-t", help="GitHub token (or set GITHUB_TOKEN env var)")
    args = parser.parse_args()

    token = args.token or TOKEN
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    print("Fetching last 12 months of contributions for", USERNAME, "…")
    months = fetch_monthly(token)

    print("\n  Month          Contributions")
    print("  " + "-" * 28)
    for y, m, c in months:
        print("  {:3s} {}   {:>5d}".format(MONTH_NAMES[m - 1], y, c))

    print()
    block = build_planets_block(months)
    if args.output:
        write_test_svg(block, args.output)
    else:
        update_svg(block)
    print("Done.")


if __name__ == "__main__":
    main()
