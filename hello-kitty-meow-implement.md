# Hello Kitty Meow Button Implementation Plan

## Overview
- A single HTML file webpage featuring a Hello Kitty-themed "Meow" button that synthesizes and plays an AI-generated cat meow sound on click.
- Status: Planned
- Target completion: TBD

## Context/Background
- **Why needed:** Fun, whimsical single-page experience showcasing procedural audio synthesis with Web Audio API.
- **Current state:** No existing webpage - new project.
- **Target state:** A single self-contained HTML file with Hello Kitty aesthetic, pure CSS illustration, and interactive meow sound.
- **Fits into:** Standalone webpage (no larger system integration).

## Research Findings

### Options Considered

#### Option: Tech Stack - Vanilla JS
**Description:** Plain JavaScript with no frameworks or build tools, single HTML file.
**Benefits:** Zero dependencies, ~0KB overhead, fastest load, direct DOM access, easiest debugging, future-proof.
**Costs:** Manual state management (minimal for single button), no built-in reactivity (not needed).
**Risks:** None significant for single-button project.
**Decision:** Chosen.

#### Option: Tech Stack - React/Vue CDN
**Description:** Using React or Vue via CDN for component structure.
**Benefits:** Familiar component patterns, reactivity system.
**Costs:** React runtime 45KB+ before user code, virtual DOM overhead for trivial UI.
**Risks:** Massive overkill for a single button; slower load time.
**Decision:** Rejected - unsuitable for single-button project.

#### Option: Tech Stack - Svelte CDN
**Description:** Using Svelte compiled via CDN approach.
**Benefits:** Small runtime, compile-time optimization.
**Costs:** Requires build step to produce single HTML file.
**Risks:** Build requirement conflicts with single-file goal.
**Decision:** Rejected - doesn't fit single-file without build.

#### Option: Meow Synthesis - FM Synthesis + Filter Sweep Combo
**Description:** Combine FM synthesis (modulator→carrier) with lowpass filter frequency sweep for realistic meow contour.
**Benefits:** Creates harmonic richness + natural pitch bend; most realistic cat meow from oscillators.
**Costs:** Requires tuning of modulator ratio and filter sweep parameters.
**Risks:** May need parameter adjustment for optimal sound.
**Decision:** Chosen (based on https://greweb.me/2013/08/FM-audio-api).

#### Option: Meow Synthesis - Formant Synthesis
**Description:** Multiple bandpass filters (700Hz, 1200Hz, 2400Hz) simulating vocal tract formants.
**Benefits:** Simulates cat vocal tract characteristics.
**Costs:** More filters to tune, higher complexity.
**Risks:** Browser performance on low-end devices.
**Decision:** Rejected - more complex without proportional benefit.

#### Option: Meow Synthesis - Simple Oscillator + Envelope
**Description:** Single oscillator with amplitude envelope, no frequency modulation.
**Benefits:** Simplest implementation.
**Costs:** Least realistic, sounds synthetic.
**Risks:** Poor audio quality.
**Decision:** Rejected - quality insufficient.

#### Option: Design - Pure CSS Hello Kitty with Bow
**Description:** CSS-only illustration of Hello Kitty face with iconic red bow, whiskers, eyes, nose.
**Benefits:** No external images; crisp at any resolution; matches Hello Kitty brand exactly.
**Costs:** CSS complexity for shapes.
**Risks:** None significant.
**Decision:** Chosen (based on https://github.com/lorenai/Hello-Kitty, https://github.com/katik/hellokitty).

#### Option: Design - Minimalist Pink Button
**Description:** Simple styled button with Hello Kitty colors, no illustration.
**Benefits:** Minimal CSS.
**Costs:** Less distinctive, less "Hello Kitty".
**Risks:** May feel generic.
**Decision:** Rejected - less engaging.

### Decision Made
- **Chosen approach:** Vanilla JS single-file HTML with pure CSS Hello Kitty illustration and FM synthesis + filter sweep meow generation.
- **Rationale:** Minimal dependencies (none), fastest load, simplest debugging, no build step. FM synthesis + filter sweep provides best quality-to-complexity ratio for procedural cat meow. Pure CSS Hello Kitty is iconic and requires no external assets.

### Risks Identified
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Safari autoplay policy: `resume()` must be called synchronously in click handler | H | H | Call `audioCtx.resume()` directly in click event handler, not in async callback |
| iOS WebKit prefix: older iOS needs `webkitAudioContext` | M | H | Use `window.AudioContext \|\| window.webkitAudioContext` |
| Chrome AudioContext suspension: starts in suspended state | H | M | Call `resume()` on first user click before `playMeow()` |
| Meow sounds robotic if FM parameters not tuned | M | M | Start with documented parameters; iterate if needed |

## Implementation Phases

### Phase 1: Create Hello Kitty HTML Structure (Est: 1 hour)
**Goal:** Single HTML file with semantic structure for Hello Kitty illustration and meow button.

#### Step 1.1: Set up HTML document structure
**Files:** `hello-kitty-meow.html`
**Actions:**
- Create HTML5 document with `<html>`, `<head>`, `<body>`
- Add meta tags: charset UTF-8, viewport for mobile
- Add title: "Hello Kitty Meow"
- Link CSS in `<head>`, JS in `<body>` before closing tag

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello Kitty Meow</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@700&display=swap" rel="stylesheet">
  <style>
    /* CSS goes here */
  </style>
</head>
<body>
  <div class="container">
    <div class="kitty">
      <!-- Hello Kitty face, ears, bow, whiskers -->
    </div>
    <button id="meow-btn" class="meow-button">Meow!</button>
  </div>
  <script>
    // JavaScript goes here
  </script>
</body>
</html>
```

#### Step 1.2: Create CSS variable theme
**Actions:**
- Define CSS custom properties for Hello Kitty palette

```css
:root {
  --color-red: #F51F27;
  --color-pink: #FFC0CB;
  --color-yellow: #FFB827;
  --color-white: #FFFFFF;
  --color-black: #000000;
  --color-bg: #ECE4ED;
}
```

### Phase 2: Implement Pure CSS Hello Kitty Illustration (Est: 2 hours)
**Goal:** CSS-only Hello Kitty face with bow, whiskers, eyes, nose - no images.

#### Step 2.1: Build Hello Kitty head and ears
**Files:** `hello-kitty-meow.html` (CSS section)
**Actions:**
- Create `.kitty` container with circular head (160px diameter)
- Position ears using absolute positioning with border-radius tricks
- White fill with black 8px border

```css
.kitty {
  position: relative;
  width: 160px;
  height: 160px;
  background: var(--color-white);
  border: 8px solid var(--color-black);
  border-radius: 50%;
}

.ear {
  position: absolute;
  width: 62px;
  height: 62px;
  background: var(--color-white);
  border: 8px solid var(--color-black);
  border-radius: 26px 62px 39px 60px;
}

.left-ear {
  top: -40px;
  left: 2px;
  transform: rotate(12deg);
}

.right-ear {
  top: -40px;
  right: 2px;
  transform: rotate(-12deg);
}
```

#### Step 2.2: Add eyes, nose, whiskers
**Actions:**
- Create `.eyes` as black ovals with rounded corners
- Create `.nose` as small yellow oval
- Create `.whiskers` as thin black rounded rectangles at angles

```css
.eye {
  position: absolute;
  width: 20px;
  height: 28px;
  background: var(--color-black);
  border-radius: 50%;
}

.left-eye { top: 50px; left: 30px; }
.right-eye { top: 50px; right: 30px; }

.nose {
  position: absolute;
  width: 20px;
  height: 14px;
  background: var(--color-yellow);
  border-radius: 50%;
  top: 85px;
  left: 70px;
}

.whisker {
  position: absolute;
  width: 60px;
  height: 6px;
  background: var(--color-black);
  border-radius: 0 20px 15px 0;
}
```

#### Step 2.3: Add iconic red bow
**Actions:**
- Create `.bow` container positioned above head
- Style `.bow-left`, `.bow-right` as oval shapes
- Style `.bow-center` as small circle

```css
.bow {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
}

.bow-left, .bow-right {
  position: absolute;
  width: 50px;
  height: 66px;
  background: var(--color-red);
  border: 6px solid var(--color-black);
  border-radius: 999px;
}

.bow-left {
  left: -35px;
  transform: rotate(22deg);
}

.bow-right {
  left: 15px;
  transform: rotate(-22deg);
}

.bow-center {
  position: absolute;
  width: 36px;
  height: 36px;
  background: var(--color-red);
  border: 6px solid var(--color-black);
  border-radius: 50%;
  left: -18px;
  top: 10px;
}
```

### Phase 3: Implement Web Audio API Meow Synthesis (Est: 2 hours)
**Goal:** Functional meow sound on button click using FM synthesis + filter sweep.

#### Step 3.1: Set up AudioContext with browser compatibility
**Files:** `hello-kitty-meow.html` (JS section)
**Actions:**
- Create AudioContext using vendor prefix fallback
- Initialize on page load
- Handle suspended state gracefully

```javascript
const AudioContextClass = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
  if (!audioCtx) {
    audioCtx = new AudioContextClass();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}
```

#### Step 3.2: Implement FM synthesis meow function
**Actions:**
- Create modulator oscillator (sine, ~150Hz)
- Create carrier oscillator (sawtooth, 600Hz start)
- Connect modulator → modulatorGain → carrier.frequency
- Add lowpass filter with frequency sweep (2000Hz → 400Hz)
- Add amplitude envelope (attack 20ms, decay 300ms)
- Schedule oscillator stop after 0.4s

```javascript
function playMeow() {
  if (!audioCtx) initAudio();
  if (audioCtx.state === 'suspended') audioCtx.resume();

  const now = audioCtx.currentTime;

  // Modulator
  const modulator = audioCtx.createOscillator();
  modulator.type = 'sine';
  modulator.frequency.value = 150;

  const modulatorGain = audioCtx.createGain();
  modulatorGain.gain.value = 50;

  // Carrier
  const carrier = audioCtx.createOscillator();
  carrier.type = 'sawtooth';
  carrier.frequency.setValueAtTime(600, now);
  carrier.frequency.exponentialRampToValueAtTime(300, now + 0.3);

  // Connect modulator → carrier frequency
  modulator.connect(modulatorGain);
  modulatorGain.connect(carrier.frequency);

  // Lowpass filter sweep
  const filter = audioCtx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(2000, now);
  filter.frequency.exponentialRampToValueAtTime(400, now + 0.3);
  filter.Q.value = 5;

  // Amplitude envelope
  const ampEnv = audioCtx.createGain();
  ampEnv.gain.setValueAtTime(0, now);
  ampEnv.gain.linearRampToValueAtTime(0.4, now + 0.02);
  ampEnv.gain.exponentialRampToValueAtTime(0.01, now + 0.35);

  // Connect: carrier → filter → ampEnv → destination
  carrier.connect(filter);
  filter.connect(ampEnv);
  ampEnv.connect(audioCtx.destination);

  // Start and stop
  modulator.start(now);
  carrier.start(now);
  modulator.stop(now + 0.4);
  carrier.stop(now + 0.4);
}
```

#### Step 3.3: Wire up button click handler
**Actions:**
- Get button element by ID
- Add click listener that calls `initAudio()` then `playMeow()`
- Ensure Safari resume requirement met (synchronous call)

```javascript
const meowBtn = document.getElementById('meow-btn');
meowBtn.addEventListener('click', () => {
  initAudio();
  playMeow();
});
```

### Phase 4: Style Meow Button (Est: 1 hour)
**Goal:** Hello Kitty-themed button matching aesthetic.

#### Step 4.1: Position and style button
**Actions:**
- Center button below Kitty illustration
- Apply Hello Kitty colors (pink background, red border)
- Round corners, bold font
- Add hover/active states

```css
.meow-button {
  margin-top: 40px;
  padding: 15px 40px;
  font-size: 24px;
  font-family: 'Quicksand', 'Nunito', sans-serif;
  font-weight: bold;
  color: var(--color-black);
  background: var(--color-pink);
  border: 6px solid var(--color-black);
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.1s;
}

.meow-button:hover {
  transform: scale(1.05);
  box-shadow: 4px 4px 0 var(--color-black);
}

.meow-button:active {
  transform: scale(0.98);
  box-shadow: 2px 2px 0 var(--color-black);
}
```

#### Step 4.2: Center content and add background
**Actions:**
- Flexbox centering for `.container`
- Hello Kitty pink/purple background color
- Add Google Font for Quicksand

```css
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--color-bg);
  font-family: 'Quicksand', 'Nunito', sans-serif;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
```

### Phase 5: Testing and Refinement (Est: 1 hour)
**Goal:** Verify functionality across browsers, tune audio quality.

#### Step 5.1: Test meow sound quality
**Actions:**
- Click button and verify audible meow
- Adjust FM parameters if sounds robotic
- Test on Chrome, Firefox, Safari

#### Step 5.2: Test mobile responsiveness
**Actions:**
- Verify layout on mobile viewport
- Test iOS Safari click handling
- Ensure touch events trigger audio

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `hello-kitty-meow.html` | Create | Single-file webpage with CSS Hello Kitty + JS meow synthesis |

## Verification Checklist

### Functional
- [ ] Page loads without errors in Chrome, Firefox, Safari
- [ ] Hello Kitty illustration renders correctly (face, ears, bow, whiskers, eyes, nose)
- [ ] Clicking "Meow!" button produces audible cat meow sound
- [ ] Button hover/active states work

### Edge Cases
- [ ] AudioContext autoplay: First click resumes suspended context and plays sound
- [ ] Safari: Sound plays on click without needing async callback
- [ ] iOS: Touch event triggers audio playback
- [ ] Rapid clicks: Multiple meows can overlap (no crash)

### Browser Compatibility
- [ ] Chrome: AudioContext.resume() called on click
- [ ] Firefox: Audio plays on click
- [ ] Safari: resume() called synchronously, not in async context
- [ ] Mobile: Touch events trigger audio

## Open Questions

- [ ] None - all decisions made during options phase

## Appendix: Relevant Documentation

- Web Audio API FM synthesis: https://greweb.me/2013/08/FM-audio-api
- Web Audio API Advanced Techniques: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques
- Chrome Autoplay Policy: https://developer.chrome.com/blog/web-audio-autoplay
- Safari AudioContext resume: https://stackoverflow.com/questions/57510426/cannot-resume-audiocontext-in-safari
- Hello Kitty Pure CSS (reference): https://github.com/lorenai/Hello-Kitty
- Hello Kitty Pure CSS Animation (reference): https://github.com/katik/hellokitty
- Hello Kitty Color Palette: https://loading.io/color/feature/HelloKitty/
