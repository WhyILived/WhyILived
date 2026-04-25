# README Build Plan

**Status:** Planning — not yet implementing  
**Goal:** A deep space / mission control themed GitHub profile README that's visually stunning, automated, and has personality

---

## What's Decided

| Decision | Choice |
|---|---|
| Theme | Deep Space / Mission Control (Option A) — dark, blues/purples, feels like a spacecraft dashboard |
| Typing animation tone | Personality-first, not a résumé |
| Setup effort | High — willing to do GitHub Actions, secrets, workflows |
| Private repo stats | Yes |
| Contribution graph | TBD — need to pick (see Section 3) |
| Bio/About section | Deferred to later |
| Full tech stack | Deferred to later |

---

## Typing Animation Phrases (from your answers)

These will cycle in the animated typewriter block at the top of the profile:

```
"My Ascendant to Iron descent needs to be studied"
"Perpetually Procrastinating"
"You've been heralded"
"I use Arch btw"
"HOW IS HE STILL PRESIDENT"
"Kapow!"
```

**OPEN QUESTION 1 — Phrase order & additions**

Quick context on each phrase so we're on the same page:
- *"My Ascendant to Iron descent..."* — Valorant rank joke (Ascendant is high rank, Iron is the lowest)
- *"Perpetually Procrastinating"* — relatable chaos energy
- *"You've been heralded"* — this sounds like it's from Hades (the game), where Hermes says it when you die. Is that right? Or is it a reference to something else? Matters because the phrasing is a bit cryptic without context and I want to make sure the vibe is what you intend
- *"I use Arch btw"* — classic Linux meme (Arch Linux users are famously proud of using it, this is the engineer version of a humble brag)
- *"HOW IS HE STILL PRESIDENT"* — political frustration, presumably about Trump. Worth confirming — this will be visible to every recruiter, professor, and potential employer who visits your profile. Still want it? (No judgment, just making sure it's intentional)
- *"Kapow!"* — what's this a reference to? Is it just vibes, or does it mean something? Spider-Man? A project? A catchphrase?

Any phrases you want to add or remove?

---

## Planned Sections (Top to Bottom)

This is the full proposed structure of your README:

```
1.  [Animated header banner]
2.  [Typing animation — personality phrases]
3.  [Short bio / intro]
4.  [Stats + languages side by side]
5.  [Tech stack badges]
6.  [Contribution graph animation]
7.  [Activity graph — 31 days]
8.  [GitHub trophies]
9.  [Animated footer + contact links]
```

Section order can be rearranged — this is just the default logic flow.

---

## Section 3 — Contribution Graph Animation Options

You said you didn't want to default to the snake — here are all the real options. Pick one (or say none and we skip it).

---

### Option A: Snake (Platane/snk)
**What it looks like:** A snake slithers across your green contribution squares eating each dot, growing longer as it goes. Loops forever.

**Space-theme compatibility:** High — you can set custom colors: dark background, bright blue or gold dots, a neon-colored snake. Looks great in space palette.

**Dark mode support:** Yes — it can serve two versions and GitHub auto-picks based on viewer's theme setting.

**Vibe:** Classic, satisfying, immediately recognizable as "that cool contribution graph thing."

**Setup:** GitHub Action runs daily, generates the SVG, saves it to the repo. Medium effort (~10 min).

**Link to see examples:** https://github.com/Platane/snk

---

### Option B: Pac-Man (abozanona/pacman-contribution-graph)
**What it looks like:** Pac-Man navigates your contribution grid eating dots, with ghosts chasing it. Based on the actual pathfinding algorithm — Pac-Man makes decisions based on the shape of your contribution graph.

**Space-theme compatibility:** Medium — supports `github-dark` and `gitlab-dark` themes but no full custom color palette. You can't make it fully space-colored.

**Vibe:** Playful, nostalgic, game-reference energy — fits your Valorant/gamer personality more than the snake does.

**Setup:** Same as snake — GitHub Action, daily regeneration. Medium effort.

**Link to see examples:** https://github.com/abozanona/pacman-contribution-graph

---

### Option C: Bubble Pop / Exploding (Man0dya/Readme-Contribution-Graph-Generator)
**What it looks like:** Your contribution dots pop and explode like bubbles or particles. Less "game" and more "visual effect."

**Space-theme compatibility:** Medium — dark mode available but limited custom colors.

**Vibe:** Unique, unusual — most people haven't seen this one. Kind of chaotic energy. Matches "Kapow!" tbh.

**Setup:** Similar to above.

**Link to see examples:** https://github.com/Man0dya/Readme-Contribution-Graph-Generator

---

### Option D: Custom Space SVG (hand-crafted)
**What it looks like:** A completely custom SVG file we write ourselves and commit to the repo — an animated star field or nebula background with your actual contribution data overlaid. Would look like no one else's profile because it doesn't use any external tool.

**Space-theme compatibility:** Maximum — we build it to spec.

**Vibe:** Most technically impressive, most unique, matches your website aesthetic the best.

**Setup:** High effort — I'd write the SVG, but it requires design decisions from you and more iteration.

**The catch:** GitHub heavily sandboxes SVG rendering — no JavaScript allowed, only CSS animations. This limits what's possible but CSS-only animations can still look incredible.

---

### Option E: Galaxy-Profile Full Suite (vinimlo/galaxy-profile)
**What it looks like:** This generates four full animated SVG panels — a spiral galaxy header with your name, a "Mission Telemetry" card with your GitHub stats displayed like spacecraft readings, a radar chart of your tech stack, and animated project cards. The contribution graph is embedded in the Mission Telemetry card.

**Space-theme compatibility:** Maximum — this is literally the space aesthetic tool.

**Vibe:** The most visually cohesive and impressive option. Would replace several other sections (stats card, activity graph, and contribution graph all become one unified design).

**Setup:** Heaviest — fork a repo, edit a config file, run a GitHub Action. Probably 30-45 minutes total. But I can write every file for you.

**Link:** https://github.com/vinimlo/galaxy-profile

---

**OPEN QUESTION 2 — Which contribution graph do you want?**

If you pick Option E (Galaxy-Profile), it changes a lot about how we structure everything else — it would replace separate stats cards and graphs with one unified space-themed suite. That might actually be the cleanest approach given you want the deep space look. But it's the most setup.

---

## Section 4 — Stats Cards

**How this works:** A URL you paste into your README that auto-generates a card image with your GitHub stats. Updates automatically. No setup beyond pasting the URL.

**Plan:** Use `tokyonight` or `synthwave` theme (both dark/space-appropriate). We'll configure it to include private repo contributions since you confirmed your GitHub account already counts those in the contribution graph.

**OPEN QUESTION 3 — GitHub Personal Access Token**

To make the stats card include private repo numbers, I need to walk you through generating a token. This takes about 5 minutes:

1. Go to github.com → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens
2. Create a token with read-only access to your repos
3. Add it as a "secret" (encrypted variable) to your WhyILived/WhyILived repo at Settings → Secrets and variables → Actions → New repository secret, name it `GH_TOKEN`

Do you want to do this step? (yes/no/walk me through it when we get there)

---

## Section 5 — Tech Stack Badges

Deferred — you said your stack on the website is outdated. **We'll come back to this after you tell me the real list.** For now I'll leave a placeholder.

**OPEN QUESTION 4 — Tech stack**

When you're ready, tell me:
- All programming languages you actively use
- Hardware platforms (microcontrollers, dev boards)
- Operating systems / embedded OSes
- Tools, IDEs, protocols, frameworks
- Anything from private projects worth showing even if people can't see the repo

No rush — this can happen mid-build.

---

## Section 6 — About / Bio Section

Deferred — you said we'd think about this later. 

**OPEN QUESTION 5 — Bio**

When you're ready, a few things I'd want to know:
- What's the story behind the username "WhyILived"? Is that public/shareable or private?
- Do you want to mention the rocket/VTOL work, hackathon wins, or keep it vague?
- Do you want it to feel like a mission briefing (space aesthetic), a terminal readout, or just casual and human?
- Any projects from private repos you want name-dropped?

---

## Section 9 — Footer & Contact Links

**Planned links (from your answer "most of those yeah"):**

| Link | Include? | Value |
|---|---|---|
| Website | Yes | wilinc.co |
| Email | Confirm which | mm22rahm@uwaterloo.ca or leaheliz18@gmail.com? |
| LinkedIn | Confirm | Do you have one? URL? |
| Twitter/X | Confirm | Do you have one? |
| Discord | Confirm | Want to share a tag? |

**OPEN QUESTION 6 — Contact links**

Which email do you want public-facing on GitHub? And fill in any of the above you want included. Anything I missed?

---

## GitHub Actions We'll Set Up

These are the automated scripts that will run on a schedule to keep your README dynamic:

| Action | What it does | Runs |
|---|---|---|
| Contribution graph animation | Generates the animated SVG of your choice | Daily |
| (Optional) WakaTime stats | Shows your coding time by language | Weekly |
| (Optional) Spotify now playing | Shows what you're listening to | Real-time |

**OPEN QUESTION 7 — WakaTime and Spotify**

**WakaTime** is a plugin you install in your code editor (VSCode, CLion, etc.) that silently tracks how much time you spend coding in each language. After a week it generates stats like "C++: 14h, Python: 6h, C: 3h." You can display this as a card on your profile. 

- Do you have WakaTime? If not, want to set it up alongside this?
- Even if you set it up now, you'd need to code for a week before the card shows anything useful.

**Spotify** shows your currently-playing (or last-played) track as a card. Some people love this, some find it too personal.

- Want Spotify on there?

---

## Files We'll Create

Once planning is done, here's everything that goes into the repo:

```
WhyILived/
├── README.md                          ← the main profile (rewritten)
├── .github/
│   └── workflows/
│       ├── snake.yml                  ← (or pacman.yml, etc.) — daily animation update
│       └── (optional) wakatime.yml   ← weekly stats update
└── assets/
    ├── github-snake-dark.svg          ← auto-generated, don't edit
    ├── github-snake-light.svg         ← auto-generated, don't edit
    └── (optional) stars-header.svg   ← custom space header if we make one
```

---

## Open Questions Summary

| # | Question | Status |
|---|---|---|
| Q1 | Confirm/tweak typing phrases (especially "heralded", "PRESIDENT", "Kapow") | **Needs answer** |
| Q2 | Which contribution graph animation? (A/B/C/D/E) | **Needs answer** |
| Q3 | GitHub token for private stats — ready to set up? | **Needs answer** |
| Q4 | Full tech stack list | Deferred |
| Q5 | Bio / about section content and tone | Deferred |
| Q6 | Contact links — which email, LinkedIn, Twitter, Discord | **Needs answer** |
| Q7 | WakaTime and/or Spotify on profile? | **Needs answer** |

---

## Build Order (once planning is complete)

1. Set up GitHub token secret (if Q3 = yes)
2. Write README.md skeleton with all sections stubbed
3. Add animated header + typing animation (zero-setup, just URLs)
4. Add stats cards + languages card
5. Add tech stack badges (once Q4 answered)
6. Add contribution graph animation + GitHub Action workflow
7. Add activity graph + trophies
8. Write bio section (once Q5 answered)
9. Add footer + contact links
10. Final pass — spacing, alignment, test on GitHub dark + light mode
