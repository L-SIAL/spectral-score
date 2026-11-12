# LH Spectral Palette (iPad app) — working notes for Claude

The user is a composer. This repo holds the iPad app's source and publishes it. While travelling
they work only on the iPad, through Claude on the web/app, so this repo is the master copy of the iPad app
until they are back at the Mac (the Mac copy is on their LH_PORTABLE drive and is synced from here later).

## The app
- One file: `ipad/lh-spectral-palette-sketchpad_vNN.html` (HTML + CSS + JS, no build step, no libraries).
- `standalone/build.py` wraps it into the installable app (adds manifest, service worker, icons). Needs Pillow.
- `.github/workflows/deploy.yml` runs build.py and publishes to https://l-sial.github.io/spectral-score/
  on every push to `main` that touches `ipad/` or `standalone/`. It takes about 1–2 minutes.
- The iPad picks up a new version when the user closes the app fully and reopens it while online.
  The version shows bottom left (`<span class="ver">vNN</span>`).
- `HANDOFF.md` = change history and design notes (newest at the end). `PARITY_TODO.md` = what the Mac
  Score Tool (Lua, in REAPER, not in this repo) still needs to match.

## How to make a change
1. `git mv` the html to the next number (v87 → v88) so there is only ever ONE html in `ipad/`.
2. Change the label `<span class="ver">vNN</span>` to the new number.
3. Make the change. Keep the existing style: plain functions, comments starting `// vNN:` that say why.
4. Check the script still parses: extract the `<script>` blocks and run `node --check` on them, if node is there.
   If you can, load it in a headless browser and check there are no errors.
5. Add a `## vNN (date)` section at the end of `HANDOFF.md` (what changed, where in the code).
6. Add the Mac counterpart to `PARITY_TODO.md` (every feature needs an iPad AND a Mac version).
7. Commit and push to `main`. If you can only push a branch, open a pull request and tell the user to tap
   **Merge** in the GitHub app or website. Then tell them: wait ~2 minutes, close the app fully, reopen,
   check the version bottom left.

## The user's rules (follow them)
- Short replies at the end of a task: the result and how to use it, a few lines. Numbered steps, one step per number.
- Every feature needs iPad AND Mac parity → note the Mac side in PARITY_TODO.md.
- Terms: "sound object" in help and docs, "Object" on the interface. Never "unit" in user-facing text
  (code identifiers and saved-file keys like `unit_library` stay as they are).
- Time is real time m:ss, never tempo. Highest resolution; 14-bit controllers wherever possible.
- Envelopes default exponential. Attacks 3 ms. Never the word "expodec".
- Keep the pure-sine sound character; colour only subtly and optionally.
- Never handle passwords, tokens or secrets. Never delete the user's files or folders.
- Don't change saved-file formats in a way older sketches can't open; add keys, don't rename them.

## Useful code landmarks
- `state` holds the sketch; `state.strokes` are the sound objects (kinds: band, splash/impulse, block, chord,
  pulse, line, cloud, arc). `toJSON()` / `fromJSON()` save and load.
- Sound: `unitVoices(s)` → voices; `engineEnvelope` adds release tails; `selectVoices` + `schedule` play them;
  Play uses a 4 s look-ahead feed. `soundDelay()` corrects Bluetooth latency.
- Envelope lanes: `targetEnv` / `setTargetEnv`, `drawLane`, lanes vol / pan / spread / mod0–2.
  v80 LFOs are written as points onto a lane: `regenLaneLfo`, `lfoBase`, settings in `lane_lfo` / `mods[i].lfo`.
- Menus under the score are built by the IIFE at the end of the script (its own `$`).
- `window.__lh` exposes test hooks (fromJSON, toJSON, unitVoices, setLaneMode, state, …).

## Private notes (read first if you can)
The private repo **L-SIAL/spectral-score-notes** has the full chat history with Claude on the Mac, the manuals,
the user's preferences and a snapshot of the Mac Score Tool. If you have access, read its README.md first.
Never copy anything from it into this public repo.

## Where we are (12 Nov 2026, last Mac session before travel)
- v91 Rotation up to ±64 turns + a Rotation lane (speed over time; below the middle = backwards).
- v90 Listening: Stereo or Binaural 3D (headphones), one HRTF panner per voice.
- Mac: rotation lane written, not yet run in REAPER.

## Earlier (10 Nov)
The newest version is the one in `ipad/`. Recent work, newest first (details in HANDOFF.md):
- v87 the play head moves while one object plays alone (▶ Object / ⇧Space).
- v86 Shape · Fan in (mirror of Fan out). v84/v85 Object panel buttons in pairs — BUT the Shape · Block buttons
  stay in their wrapping row: in pairs they were unreadable on the iPad. Check readability on an iPad-sized panel.
- v83 Move / Copy to layer (K / ⇧K). v82 lane marks sit at the object's start and scroll with it.
- v80/v81 LFO on any lane (loudness, pan, spread, modulation), REAPER automation-item style, from Shape ▾ › LFO;
  the word "tremolo" is gone everywhere; Reset is now called Clear.
- v78/v79 "unit" → "object" / "sound object"; help window has a search box.
- v77 the "iPad had stopped the sound" check no longer fires by mistake (the iPad's audio clock moves in chunks).
- v76 Reverse loudness shape; v75 band release tails fixed.

Decisions and preferences from the user:
- Release tails come from the sound preset's release; an envelope that ends at silence has no tail. A per-object
  tail control was discussed and postponed ("too complicated for now") — don't build it unless asked.
- Mute / solo only need to work from the next Play, not live while playing.
- The sound must stay reasonably rich but light enough for the iPad (Playback detail setting); pure sines,
  no per-layer noise/FM colouring by default.
- The user tests on the iPad and reports back, often with screenshots. After every deploy tell them to wait ~2 min,
  close the app fully and reopen; the version bottom left must change.
- If unsure what they want, give 2–3 short options (a mockup if it's visual) before building.

Agreed but not built yet (do only when asked):
- ⏮ Return to 0:00 (button by Play, and Return/Home) that also scrolls the view to the start.
- [ ] zoom keeps the play head in the middle of the screen (pinch keeps its finger anchor).
- The duration box applies on blur, so ticking/unticking "Stretch" after typing a new length stretches the score:
  make it apply on Return only, or ask before stretching.
- The "1" key reportedly didn't hide the envelope panel once (unexplained).
- Undecided: a Focus toggle that hides panels and lanes for drawing.
