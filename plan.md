# README Build Plan

**Status:** Planning — not yet implementing  
**Goal:** A deep space / mission control themed GitHub profile README that's visually stunning, automated, and has personality

---

## What's Decided

| Decision | Choice |
|---|---|
| Theme | Deep Space / Mission Control — dark, blues/purples, feels like a spacecraft dashboard |
| Typing animation tone | Personality-first, not a résumé |
| Setup effort | High — willing to do GitHub Actions, secrets, local machine scripts |
| Private repo stats | Yes |
| Contribution graph | Custom hand-written space SVG |
| Live status badge | Yes — Arch Linux / Hyprland "last seen" or "now online" |
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

**OPEN QUESTION 2 — hypridle setup details**

Before I write the scripts, I need to know:
- Do you currently use `hypridle`? (Run `which hypridle` or `pgrep hypridle` in your terminal — if it returns something, you have it)
- Do you use a screen locker like `hyprlock` or `swaylock`? The on_lock_cmd hook fires when your screen locks, which is the cleanest trigger for "went offline"
- Alternative trigger: instead of lock/unlock, we could use **login/logout** via a systemd user service. This means the badge updates when you boot up (online) and shutdown (offline) rather than every time you lock your screen. Which feels more accurate to you?
- How precise do you want "last seen"? Options:
  - `Last seen 3h ago` (calculated from timestamp in the Gist)
  - `Last seen today` (less precise, more casual)
  - Just `Offline` with no time info

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

**OPEN QUESTION 3 — Which SVG direction?**

Which of A/B/C/D feels most "you"? Or describe something else entirely. You can also say "surprise me" and I'll pick based on your website aesthetic.

Note: for Options A/B/C that use your actual contribution data, the SVG will be static (a snapshot of your current contribution graph baked in at write time). To make it auto-update with real data we'd need a GitHub Action — doable, just more work. Worth it?

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
| Q2 | hypridle setup: do you have it, what locker do you use, login vs lock trigger, time precision | **High — needed to write status scripts** |
| Q3 | Custom SVG direction: A (stars) / B (orbits) / C (nebula grid) / D (warp) / surprise me | **High — needed to design the SVG** |
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

## Build Order (once Q2 and Q3 are answered)

1. Create the Gist + write status scripts + edit hypridle config (live status feature)
2. Walk through GitHub token setup for private stats (Q4)
3. Write README.md skeleton — all sections stubbed with placeholders
4. Add animated header (capsule render)
5. Add typing animation
6. Add live status badge
7. Add stats cards + languages side by side
8. Add activity graph + trophies
9. Build custom space SVG (contribution visualization) — biggest creative chunk
10. Add footer with placeholder contact links
11. Tech stack badges (once Q6 answered)
12. Bio section (once Q7 answered)
13. Contact links finalized
14. Final pass — spacing, alignment, test dark + light mode on GitHub
