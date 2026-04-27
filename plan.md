# README Build Plan

**Status:** In progress — building  
**Goal:** A deep space / mission control themed GitHub profile README that's visually stunning, automated, and has personality

---

## What's Decided

| Decision | Choice |
|---|---|
| Theme | Deep Space / Mission Control — dark, blues/purples, feels like a spacecraft dashboard |
| Typing animation tone | Personality-first, not a résumé |
| Setup effort | High — willing to do GitHub Actions, secrets, local machine scripts |
| Private repo stats | Yes |
| Contribution graph | Custom hand-written SVG — Orbital System (CSS animated planets orbiting a star) |
| Live status badge | Yes — Arch Linux / Hyprland, "Online" or "Offline" (no timestamp) |
| Bio/About section | Deferred |
| Full tech stack | Deferred |
| WakaTime | No |
| Spotify | No |
| Contact links | Placeholders for now, finalize later |

---

## Typing Animation Phrases ✓

Confirmed as-is:

```
"My Ascendant to Iron descent needs to be studied"
"Perpetually Procrastinating"
"You've been heralded"
"I use Arch btw"
"HOW IS HE STILL PRESIDENT"
"Kapow!"
```

**OPEN QUESTION 1 — A few quick clarifications on the phrases**

No blocking issues, just want to make sure intent is right before locking these in:

- *"You've been heralded"* — is this a Hades (the game) reference? Hermes says it when you die. Or is it something else? Doesn't change whether we use it, just want to know if there's a deeper meaning behind it
- *"HOW IS HE STILL PRESIDENT"* — flagging once more: this will be the first thing people see on your GitHub profile including recruiters, professors, internship hiring managers. Still fully your call — just making sure it's intentional and not something you'd want to swap for something less politically tied. Options if you want an alternative vibe: "why is it still winter", "genuinely confused", etc.
- *"Kapow!"* — pure vibes, or a reference to something specific?

---

## Planned Sections (Top to Bottom)

```
1.  [Animated space header banner]
2.  [Typing animation — personality phrases]
3.  [🟢 Live status: Online / Last seen on Arch Linux / Hyprland]
4.  [Short bio / intro]                              ← deferred
5.  [Stats card + Top languages card — side by side]
6.  [Tech stack badges]                              ← deferred
7.  [Activity graph — 31 days]
8.  [Custom space SVG — contribution visualization]
9.  [GitHub trophies]
10. [Animated footer + contact links]
```

---

## Section 3 — Live Status Badge (Arch Linux / Hyprland)

**Decision:** Yes, building this.

**What it'll show:**
- When you're active: `🟢 Online · Arch Linux / Hyprland`
- When idle/locked: `⚫ Last seen · Xh Xm ago`

**How the full pipeline works:**

```
hypridle detects screen lock/unlock on your machine
        ↓
Fires on_lock_cmd or on_unlock_cmd shell hooks
        ↓
Shell script runs: calls GitHub API to update a Gist (a small hosted text file)
        ↓
Gist contains JSON: { "schemaVersion": 1, "label": "status", "message": "Online · Arch / Hyprland", "color": "brightgreen" }
        ↓
README badge URL points to shields.io which reads the Gist live
        ↓
Visitor sees a live badge — updates within minutes of your status changing
```

**Files needed on your machine (I'll write all of these):**
```
~/.local/bin/github-status-online.sh     ← called when you unlock / resume
~/.local/bin/github-status-offline.sh   ← called when screen locks / goes idle
```

**Edit needed in your hypridle config:**
```
~/.config/hypr/hypridle.conf
```
We add `on_lock_cmd` and `on_unlock_cmd` lines pointing to those scripts.

**Files needed in the repo:** None new — just a badge URL in README.md.

**Secrets needed:** One GitHub token with `gist` write permission (separate from the stats token, or can be the same token if you give it both permissions).

**Q2 — ANSWERED**
- Has hypridle: yes
- Screen locker: DMS (also has hyprlock but doesn't use it)
- Status precision: just "Offline" — no timestamp
- Implementation: using hypridle `listener` block with `on-timeout` / `on-resume` hooks (fires after 10 min idle → offline, fires on resume → online). This works regardless of which locker is used since it's based on idle detection, not lock events.

---

## Section 4 — Custom Space SVG (Contribution Visualization)

**Decision:** Custom hand-written SVG, not a third-party tool.

**What it'll be:** An animated SVG that visualizes your GitHub contribution data in a space aesthetic. Think: a dark starfield where your contribution activity is represented as glowing stars or orbital paths — more intense contribution weeks = brighter/bigger elements.

**The GitHub SVG constraint:** GitHub strips JavaScript from SVGs for security. Only CSS animations work. CSS can do: fade in/out, pulse, scale, color cycle, translate (movement), rotation. That's enough for a proper space animation.

**Design directions — pick one:**

**Option A — Star Field**
Your contributions become a field of stars, twinkling with CSS animations. Higher-activity weeks are brighter/larger stars. The background is a deep space gradient. Looks like looking out a spaceship window.

**Option B — Orbital System**
Each week of contributions becomes a planet orbiting a central star. Activity level determines planet size. CSS keyframe animation makes them orbit continuously. Very clean, very "mission control."

**Option C — Nebula / Pulse Grid**
The contribution grid is kept as a grid but each cell glows and pulses like a nebula cloud. Empty days are dark, active days pulse with blue/gold light. More abstract, closest to a data visualization aesthetic.

**Option D — Warp Speed**
Stars stream past horizontally — pure CSS animation of white lines on black. Your contribution data controls the density of stars. Feels like warp/hyperspace. No grid at all.

**Q3 — ANSWERED: Surprise me → Orbital System (Option B)**
CSS-animated orbital system: a glowing central star with rings, each week of contribution activity represented as a planet on an orbital path. Activity level determines planet size. All pure CSS keyframe animations — no JavaScript. Decorative (not live data-driven) — sits alongside the activity graph which shows real data.

---

## Section 5 — Stats Cards

**Plan:** Use `github-readme-stats` with a deep space custom color scheme (matching our palette exactly) rather than a preset theme.

**Layout:** Side by side — Stats card on left, Top Languages on right. In GitHub-flavored Markdown, true side-by-side requires an HTML table. That's fine — GitHub renders basic HTML tables in READMEs.

**Private stats:** Already enabled on your GitHub account. The stats card service just needs a token to see it — handled in the token setup step.

**OPEN QUESTION 4 — Stats token setup**

This is the step where you generate a Personal Access Token on GitHub so the stats card can read your private repo data. It's a 5-minute process:

1. Go to: `github.com/settings/tokens` → "Fine-grained tokens" → "Generate new token"
2. Set expiration (I'd suggest 1 year or no expiration)
3. Give it read access to your repositories
4. Copy the token (it only shows once)
5. Go to your `WhyILived/WhyILived` repo → Settings → Secrets and variables → Actions → New repository secret
6. Name: `GH_TOKEN`, Value: the token you just copied

Ready to do this step now, or save it for when we're building?

---

## Section 6 — Tech Stack Badges

Deferred. When you're ready, tell me:
- All programming languages you actively use (not just C/C++/Python from the website — what else?)
- Hardware platforms (microcontrollers, dev boards, FPGAs?)
- OSes / embedded OSes / RTOSes
- Tools, IDEs, build systems, protocols
- Anything from private projects worth showing

---

## Section 7 — Activity Graph

**Plan:** Use `github-readme-activity-graph` with the `tokyo-night` theme. It's dark, blue-tinted, and fits the space palette well. No setup required — just a URL.

---

## Section 9 — GitHub Trophies

**Plan:** Use `github-profile-trophy` with the `darkhub` or `onedark` theme. Dark-appropriate, shows achievements like commit streaks, stars, PRs. No setup required — just a URL.

---

## Section 10 — Footer & Contact Links

**Placeholders for now — to finalize later:**

| Link | Status |
|---|---|
| Website (wilinc.co) | ✓ confirmed |
| Email | TBD — which one? |
| LinkedIn | TBD — URL? |
| Twitter/X | TBD — handle? |
| Discord | TBD — tag? |

**OPEN QUESTION 5 — Contact details (no rush)**

Which email do you want public? Do you have LinkedIn/Twitter/Discord you want linked?

---

## Section 1 — Animated Header

**Plan:** Capsule Render with `venom` or `blur` shape type. Custom gradient in the space palette (`#0d1117` → `#1a0533` → `#0d2137`). Text: `WhyILived` with `twinkling` animation. A subtitle line: `why i lived.` in smaller text.

No open questions here — this is fully plannable from what we know.

---

## Section 2 — Bio

Deferred. **OPEN QUESTION 6 — Bio (no rush)**

When ready:
- What's the story behind the username "WhyILived"? Public or private?
- Mission briefing tone, terminal readout, or casual human?
- Rocket/VTOL work, hackathons — mention or leave vague?
- Private projects worth name-dropping?

---

## Open Questions Summary

| # | Question | Priority |
|---|---|---|
| Q1 | Clarify "heralded" reference, confirm "PRESIDENT" phrase, explain "Kapow" | Low — not blocking |
| Q2 | hypridle setup details | ✓ Answered — using listener/timeout approach |
| Q3 | Custom SVG direction | ✓ Answered — Orbital System |
| Q4 | GitHub token for private stats — now or during build? | Medium |
| Q5 | Contact link details (email, LinkedIn, Twitter, Discord) | Low — deferred |
| Q6 | Bio content and tone | Low — deferred |

---

## Files We'll Create

```
WhyILived/WhyILived repo:
├── README.md                            ← completely rewritten
├── .github/
│   └── workflows/
│       └── (optional) update-svg.yml   ← if we auto-update the space SVG
└── assets/
    ├── space-contributions.svg          ← custom animated SVG
    └── (optional) header.svg           ← custom animated header

Your local Arch Linux machine:
├── ~/.local/bin/github-status-online.sh
└── ~/.local/bin/github-status-offline.sh
~/.config/hypr/hypridle.conf            ← edited, not created

GitHub (external):
└── A Gist (small hosted JSON file)     ← stores your online/offline status
```

---

## Build Progress

| Step | Status | Notes |
|---|---|---|
| Update plan/research docs | ✅ Done | |
| Write orbital.svg | ✅ Done (SVG bug fixed) | `assets/orbital.svg` — kept in assets, not in README |
| Write status scripts | ✅ Done | `local-scripts/` — online.sh, offline.sh, hypridle-addition.conf |
| Write README.md | ✅ Done | Revised per feedback |
| Animated header | ✅ Done | venom, space gradient, no animation (simplified) |
| Typing animation | ✅ Done | 6 phrases, Fira Code font |
| Status + visitor badges | ❌ Removed | User requested removal |
| Stats + top languages cards | ❌ Removed | Replaced by tech stack badges |
| Tech stack badges | ✅ Partial | C, C++, Python, Arch, FreeRTOS, Git, Linux — **needs full list from you** |
| Activity graph | ✅ Done | custom space colors |
| Pac-Man contribution graph | ✅ Done in README | **Needs workflow run — see below** |
| Pac-Man GitHub Action | ✅ Done | `.github/workflows/pacman.yml` |
| GitHub trophies | ✅ Done | darkhub theme |
| Footer (capsule render wave) | ✅ Done | |
| Bio section | ⏳ Deferred | waiting on content |
| Contact links | ⏳ Deferred | waiting on details |
| Full tech stack badges | ⏳ Deferred | waiting on your full list |
| Final pass + dark/light mode test | ⏳ After deferred sections done | |

---

## ⚡ Action Required: Live Status Setup

These are the steps you need to do on your end to activate the status badge. Takes ~10 minutes.

### Step 1 — Create a GitHub Gist

1. Go to **https://gist.github.com**
2. Filename: `status.json`
3. Content (paste exactly):
   ```json
   {"schemaVersion":1,"label":"status","message":"Offline","color":"555555","namedLogo":"linux","logoColor":"white"}
   ```
4. Set to **Secret** (or Public — both work)
5. Click **Create secret gist**
6. Copy the **Gist ID** from the URL — it's the long alphanumeric string after your username:
   `https://gist.github.com/WhyILived/`**`abc123def456...`** ← that part

### Step 2 — Create a GitHub Token

1. Go to **https://github.com/settings/tokens** → "Generate new token (classic)"
2. Name: `github-status-badge`
3. Expiration: No expiration (or 1 year)
4. Scopes: tick **`gist`** only (that's all it needs)
5. Click **Generate token**
6. Copy the token immediately — it only shows once

### Step 3 — Create the config file on your machine

```bash
mkdir -p ~/.config/github-status
chmod 700 ~/.config/github-status

cat > ~/.config/github-status/config << 'EOF'
GIST_ID=paste_your_gist_id_here
GITHUB_TOKEN=paste_your_token_here
EOF

chmod 600 ~/.config/github-status/config
```

### Step 4 — Copy the scripts

```bash
cp local-scripts/github-status-online.sh  ~/.local/bin/github-status-online.sh
cp local-scripts/github-status-offline.sh ~/.local/bin/github-status-offline.sh
chmod +x ~/.local/bin/github-status-online.sh
chmod +x ~/.local/bin/github-status-offline.sh
```

### Step 5 — Edit hypridle.conf

Open `~/.config/hypr/hypridle.conf` and add the contents of `local-scripts/hypridle-addition.conf`. If you already have a `general {}` block, just add the `lock_cmd` and `unlock_cmd` lines to it (don't duplicate the block).

Then reload: `killall hypridle && hypridle &`

### Step 6 — Test it

```bash
# Test online script manually
~/.local/bin/github-status-online.sh

# Check your Gist — it should now say "Online"
# Then test offline:
~/.local/bin/github-status-offline.sh
```

### Step 7 — Update README.md

Replace `GIST_ID_HERE` in README.md with your actual Gist ID.
