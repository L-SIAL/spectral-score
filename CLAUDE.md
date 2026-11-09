# LH Spectral Palette (iPad app) — working notes for Claude

The user (Lawrence) is a composer. This repo holds the iPad app's source and publishes it. While travelling
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
