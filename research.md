# GitHub Profile README — Research Report

## Who You Are (pulled from wilinc.co)

- **Name:** Mushfiqur Shadhin (username: WhyILived / WIL)
- **Degree:** Computer Engineering @ University of Waterloo, graduating 2028
- **Current job:** Firmware Engineer at Georgia Tech's Propulsive Landers — building stabilization controls for VTOL (vertical take-off and landing) systems, integrating 16 sensors
- **Past:** Head of Aerodynamics & GNC at AERD — built rocket flight computers with active fin stabilization, got coverage in 45+ news outlets
- **Hackathons:** Won HackTheNorth 2025 and Hack the Valley X; ranked 7th in HackTheNorth CTF out of 1,338 competitors
- **Languages:** C, C++, Python
- **Hardware:** ESP32, Teensy, FreeRTOS, SPI/I2C protocols, JTAG
- **Other:** Founded 3 STEM clubs with 350+ members; countrywide highest grade in CS
- **Human:** Ascendant Valorant player, cat person
- **Public GitHub repos (pinned):** FATELESS_Studios, BeyondSight, DualWield — all Python

---

## What a GitHub Profile README Actually Is

Your GitHub profile has a special hidden trick: if you create a repository with the exact same name as your username (in your case, `WhyILived/WhyILived`), GitHub will display the `README.md` file from that repo at the top of your profile page — like a personal homepage. Right now yours just has the default placeholder template with everything commented out. This is what we're redesigning.

---

## The Full Toolkit — Every Tool We Could Use

### 1. Capsule Render (Animated Header/Footer Banners)
**What it is:** A free service that generates animated image banners you can embed in your README using a simple URL link. No code needed — you just construct a URL with parameters and paste it in as an image.

**Why it's great for space themes:** It supports custom color gradients (so you can do deep purple → space blue → black), and has shape types like `venom` (sharp, aggressive), `wave` (flowing), `blur` (soft glow), and `shark` that look very space/sci-fi. You can also animate the text on it with a "twinkling" effect.

**Example of what the URL looks like:**
```
https://capsule-render.vercel.app/api?type=venom&color=0:0d1117,50:1a0533,100:0d2137&text=WhyILived&animation=twinkling
```

**Setup effort:** Zero. Just paste a URL.

---

### 2. Readme Typing SVG (Animated Typewriter Text)
**What it is:** Another free URL-based service that generates a looping animated GIF/SVG that looks like someone is typing and deleting text. You embed it like an image. It cycles through a list of phrases you define.

**Why it's useful:** Instead of a static title, your profile could show phrases like "Firmware Engineer" → delete → "Rocket Builder" → delete → "CTF Hacker" → etc., cycling forever.

**Example:**
```
https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=58A6FF&lines=Firmware+Engineer;Rocket+Builder;CTF+Hacker;UWaterloo+CE+%2728
```

**Setup effort:** Zero. Just paste a URL.

---

### 3. GitHub Stats Cards (github-readme-stats)
**What it is:** A free service that reads your public GitHub data and generates a card image showing your stats — total commits, pull requests, issues, stars earned, and a "rank" grade. There's also a "top languages" card that shows which programming languages you use most across your repos.

**Themes available:** The themes `tokyonight`, `radical`, `synthwave`, and `cobalt` all have dark, vibrant, space-appropriate color schemes.

**Important caveat:** By default it only counts your *public* repos. To include your private repo contributions, you'd need to add a GitHub token (a personal access key) as a secret in this repo — more on this in the questions file.

**Setup effort:** Low. Just paste a URL. Optional extra step for private repo stats.

---

### 4. Snake Contribution Graph
**What it is:** A GitHub Action (an automated script that runs on a schedule) that looks at your contribution graph — the green squares calendar on your GitHub profile — and generates an animated SVG of a snake eating all the dots. It regenerates automatically every day and saves the animation file to your repo, which your README then displays.

**Why it's cool:** It's one of the most recognizable "impressive GitHub profile" features. The snake winds through your actual commit history.

**Dark mode support:** You can have two versions (light and dark) and GitHub will automatically show the right one based on the viewer's GitHub theme.

**Setup effort:** Medium. Requires adding a GitHub Actions workflow file (a YAML config file) to the repo. I can write this for you entirely — you'd just need to commit it.

---

### 5. Activity Graph
**What it is:** Similar to the stats card — a URL-based service that generates a line/bar graph of your GitHub activity over the last 31 days. Shows your commit frequency visually.

**Dark themes:** `tokyo-night`, `dracula`, `nord` — all space-appropriate.

**Setup effort:** Zero. Just paste a URL.

---

### 6. GitHub Profile Trophy
**What it is:** Auto-generated "achievement badge" cards based on your GitHub history — things like number of commits, repos, stars, pull requests, followers. Looks like a trophy case.

**Setup effort:** Zero. Just paste a URL.

---

### 7. Tech Stack Badges (Shields.io)
**What it is:** Small rectangular icon badges that show your tech stack. You've probably seen these on repos — little colored pills that say "Python" or "C++" with an icon. Shields.io generates them via URL.

**Why it matters:** For a firmware/embedded engineer your stack is unusual and impressive — C, C++, Python, ESP32, FreeRTOS, JTAG, SPI, I2C. Showing this visually is much better than writing a list.

**Setup effort:** Zero. Just paste URLs.

---

### 8. Galaxy-Profile (Full Animated Galaxy SVG)
**What it is:** A tool that generates animated space-themed SVG graphics (think: spiral galaxy with your name, a "Mission Telemetry" card with your GitHub stats as if they're spacecraft readings, a radar chart of your tech stack). These are genuinely gorgeous and unique.

**The catch:** It requires forking the repo (making your own copy of it on GitHub), editing a config file with your info, and letting a GitHub Action generate the SVGs. More setup than the URL-based tools but the result is far more visually impressive.

**Setup effort:** High-ish. Maybe 20 minutes of setup. I can guide you through it or write all the files.

---

### 9. Visitor Counter
**What it is:** A tiny badge that counts how many people have viewed your profile. Small touch, but satisfying.

**Setup effort:** Zero. Just paste a URL.

---

## Proposed Profile Structure

Here's the layout being considered, top to bottom:

```
╔══════════════════════════════════════════════════╗
║  [Animated space banner — capsule render header] ║
║  [Typing SVG: cycling phrases about you]         ║
╠══════════════════════════════════════════════════╣
║  Short punchy bio (1-3 sentences, space vibes)   ║
╠══════════════════════════════════════════════════╣
║  LEFT COLUMN          │  RIGHT COLUMN            ║
║  • About me bullets   │  GitHub Stats Card       ║
║  • What I'm building  │  Top Languages Card      ║
╠══════════════════════════════════════════════════╣
║  Tech stack badges (C, C++, Python, ESP32, etc.) ║
╠══════════════════════════════════════════════════╣
║  Activity graph (31-day contribution view)       ║
╠══════════════════════════════════════════════════╣
║  Snake eating your contribution graph            ║
╠══════════════════════════════════════════════════╣
║  Trophy case (your GitHub achievements)          ║
╠══════════════════════════════════════════════════╣
║  [Animated space banner — footer]                ║
║  Contact / links                                 ║
╚══════════════════════════════════════════════════╝
```

---

## Color Palette Being Considered

| Role            | Hex       | Description                      |
|-----------------|-----------|----------------------------------|
| Background      | `#0d1117` | GitHub's own dark background     |
| Deep space      | `#1a0533` | Dark purple — feels like nebula  |
| Space blue      | `#0d2137` | Deep navy blue                   |
| Star blue       | `#58a6ff` | Bright blue — GitHub accent      |
| Star gold       | `#e6b450` | Warm gold — like a distant sun   |
| Highlight green | `#39d353` | GitHub contribution green        |

---

## Sources & Further Reading

- [awesome-github-profile-readme](https://github.com/abhisheknaiidu/awesome-github-profile-readme) — curated gallery of impressive profiles
- [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) — stats cards
- [Platane/snk — Snake Graph](https://github.com/Platane/snk) — contribution snake
- [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) — typing animation
- [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) — animated banners
- [vinimlo/galaxy-profile](https://github.com/vinimlo/galaxy-profile) — full galaxy SVG suite
- [github-readme-activity-graph](https://github.com/Ashutosh00710/github-readme-activity-graph) — activity graph
- [DEV Community: GitHub aesthetics guide](https://dev.to/annavi11arrea1/github-page-aesthetics-and-fun-snake-stats-icons-and-videos-1dd7)
