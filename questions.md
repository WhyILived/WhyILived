# Questions Before We Build

These are the things I need to know before writing your README. Each question has context explaining what it means and why it matters. Answer however you like — even rough notes are fine.

---

## Q1: What phrases do you want in the animated typing text?

**What this is:**
Near the top of your profile there'll be an animated block of text that looks like someone is typing and deleting phrases on repeat. Think of it like a subtitle under your name that cycles through different things about you.

**Why it matters:**
This is often the first thing people read after your name. It should capture your identity in quick punchy bursts — the things you'd put in a bio if you had five words each time.

**Some options based on what I know about you:**
- `Firmware Engineer`
- `Rocket Scientist`
- `CTF Hacker`
- `UWaterloo CE '28`
- `Embedded Systems Nerd`
- `VTOL Control Systems`
- `Building things that fly`
- `Ascendant Valorant player` (if you want personality in there)
- `Why I Lived` (a nod to your username/identity)

**My suggestion:** Pick 4–6. A mix of professional and personality works best.

**Your answer:**

---

## Q2: Do you want the snake contribution graph?

**What this is:**
Your GitHub profile already has a "contribution graph" — that grid of green squares showing which days you made commits (code uploads). The snake tool takes that grid and animates a snake that slithers through it eating all the dots, regenerating every day automatically.

To make it work, I'd need to add a small config file to your repo called a **GitHub Actions workflow**. Think of GitHub Actions like scheduled automated tasks — in this case, it runs once a day, generates the snake animation as a file, and saves it to your repo. Your README then displays that file as an animation.

**Why it matters:**
It's one of the most visually impressive things on a GitHub profile and it's directly tied to *your actual activity* — the more you code, the more the snake has to eat.

**What I'd need to do:**
- Add a file at `.github/workflows/snake.yml` (a small config I'll write entirely)
- Add a folder to store the generated animation file
- Update your README to display it

**The catch:**
GitHub Actions needs permission to write files to your repo. By default your repo should allow this, but if it's turned off you'd get an error and need to flip a setting in your repo's Settings tab. I'll flag if that's needed.

**Your answer (yes / no / unsure):**

---

## Q3: Do you want your private repo stats included in your GitHub stats card?

**What this is:**
The stats card shows things like: total commits, pull requests, stars earned, and a rank. By default it can only see your *public* repos — the ones anyone can view. Most of your cool projects sound like they're in private repos.

To include private repo data, the stats card service needs a **GitHub Personal Access Token** — think of it like a special password you generate that gives the service read-only access to your account data (not your code, just the activity numbers).

**How it works:**
1. You generate a token at github.com/settings/tokens (I'll give exact steps)
2. You add it as a "secret" in your `WhyILived/WhyILived` repo (Settings → Secrets → Actions). A secret is stored encrypted and never visible once saved — it's the standard safe way to pass credentials to automated tools on GitHub.
3. The stats card reads it when generating your card

**Why it matters:**
If most of your commits are in private repos and you leave this off, your stats card might look sparse — showing very little activity even though you're actively building things. With the token it shows your real numbers.

**Your answer (yes / no / unsure):**

---

## Q4: How much setup are you willing to do on your end?

**Context:**
The tools fall into two categories:

**Zero-setup tools** (I write the README, you paste it in, done):
- Animated header banner
- Typing animation
- Stats cards
- Activity graph
- Trophy case
- Tech stack badges
- Visitor counter

**Medium-setup tools** (requires adding files to the repo and flipping a setting or two on GitHub):
- Snake contribution graph (adds one config file, takes ~5 min)
- Private repo stats (generate a token, paste it as a secret, ~5 min)

**Heavy-setup tools** (genuinely impressive, but 20–30 min of back-and-forth):
- Galaxy-Profile — generates full animated SVG galaxy cards with your stats styled as "Mission Telemetry." This looks unlike anything most people have. Requires forking a repo, editing a config file, and letting a GitHub Action do its thing.

**Your answer:** How much effort are you willing to put in? (just paste a file / a bit of setup is fine / let's do everything)

---

## Q5: What do you want to say in your bio / about section?

**What this is:**
A short block of text — maybe 2–4 sentences or a few bullet points — that introduces who you are and what you're about. This sits near the top of your profile and is the human-readable "hello" before all the fancy widgets.

**Why the tone matters:**
Your website has a very confident, capable, "I build real things" energy. Your GitHub bio should match that. It shouldn't sound like a resume bullet list, but also shouldn't be vague. Think: how would you introduce yourself to another engineer at a hackathon at 2am?

**Things I could include based on your background:**
- Building VTOL stabilization firmware at Georgia Tech
- Rocket flight computers with 87% stability improvement
- HackTheNorth 2025 winner
- UWaterloo Computer Engineering
- CTF competitor (7th/1338)
- The "why I lived" angle / meaning behind the username if you want to share it

**Questions within this question:**
- Do you want it to be purely professional, or include personality (Valorant, cats)?
- Is there a story behind your username "WhyILived" you'd want on there?
- Any specific projects from private repos you want name-dropped even if people can't see them?

**Your answer:**

---

## Q6: What's your tech stack — full version?

**What this is:**
There'll be a row of small colored badge icons showing your tools and languages. I know the basics from your website but want to make sure I'm not missing anything or including things you don't actually use.

**What I know so far:**
- Languages: C, C++, Python
- Microcontrollers/Hardware: ESP32, Teensy
- Protocols: SPI, I2C, JTAG
- OS/RTOS: FreeRTOS
- Tools: presumably Git, maybe VSCode or CLion?

**What I'm unsure about:**
- Do you use any web/scripting tools (JavaScript, Bash, etc.)?
- Any simulation or modeling tools (MATLAB, Simulink)?
- Any cloud or data tools (for the CTF or projects)?
- Any specific IDEs or dev tools you'd want shown?
- Anything from your private projects that's worth including?

**Your answer:**

---

## Q7: Do you want a space/galaxy visual theme or something more personal to you?

**What this is:**
"Space-themed" was your starting direction, but there's a range within that:

**Option A — Deep Space / Mission Control**
Dark backgrounds, blues and purples, star colors. Professional, clean, feels like a spacecraft dashboard or NASA terminal. Matches your aerospace/firmware background perfectly.

**Option B — Sci-Fi / Cyberpunk Space**
Neon accents, electric blues and magentas, more aggressive and edgy. Feels more hacker/CTF than aerospace.

**Option C — Something totally different**
Maybe you want a different direction entirely — some people do retro terminal green-on-black, others do minimalist monochrome, some do bold and colorful.

**My recommendation:**
Option A. Your actual work — VTOL systems, rocket engines, embedded firmware — is genuinely aerospace-adjacent, so the "mission control" aesthetic feels earned rather than just aesthetic. But you know your vibe better than I do.

**Your answer:**

---

## Q8: What links do you want in the footer / contact section?

**What this is:**
At the bottom of your profile there'll be a section with ways to reach you or learn more. This is usually a row of icon badges linking to your various accounts.

**Options to include:**
- Your website: wilinc.co
- Email: mm22rahm@uwaterloo.ca (or do you prefer leaheliz18@gmail.com or something else?)
- LinkedIn (if you have one)
- Twitter/X (if relevant)
- Discord (some engineers put this)
- Anything else?

**Your answer:**
