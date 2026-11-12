# LH Spectral Palette: handoff for Mac development and return to iPad

*Prepared 2 November 2026 from the iPad session "LH Sandstorm synth: FM, combs, iPad painter". For the user.*
*Start the Mac session in the home folder with Remote Control on, then say: "Read LH_Palette_Handoff/HANDOFF.md and continue."*

---

## 0. What's in this package

| File | What it is |
|---|---|
| `HANDOFF.md` | This document: principles, everything built, the file format, the Mac plan, and the route back to the iPad. |
| `ipad/lh-spectral-palette-sketchpad.html` | The iPad sketchpad, version 14: the reference implementation. Live copy: https://claude.ai/artifact/UdUbHCZmrfRipnk4qcpvz9 |
| `ipad/example_sketch.json` | A complete sketch file that uses every feature: bands, splashes, envelopes, a per-note envelope, a shaped outline, notes and annotations. |
| `reference_core_maths.js` | The maths the Mac version must match, extracted from the iPad source: field, band weights, splash timing, envelopes and curves, glissando outlines, point reduction. |

Related earlier material from the same session: `LH_Sandstorm.zip` (Sandstorm synth audio examples, Word manual, chat transcript). Also the Spectral Palette overview of 4 October and its design canvas: https://claude.ai/artifact/81W1WFXpiYmJqb7TS6Shvw

---

## 1. Principles to keep

1. **A working environment, not a representation.** A sonogram shows what a sound is; a DAW organises how it's produced. The Palette is a place to think in. As in architecture and design, where plans and diagrams carry their makers' annotations, ideas are captured in the moment, on the material itself, and **travel with it** from the iPad sketch to the Mac and into the piece.
2. **Drawing the sound directly.** In the UPIC tradition, the drawing is constitutive: it specifies the sound, rather than describing it (Smalley, Blackburn) or instructing a performer (Hope). The difference from UPIC is that a unit is a structured object (partials in a field, envelopes, outline, bandwidth, layer, space), so a single gesture can describe a whole spectromorphological event.
3. **Independent of any particular sound.** The score is MIDI. It's tailored to the LH synths, but any instrument in REAPER (ReaSamplOmatic5000, any VSTi) can realise it. REAPER is being recast as a **graphic-notation environment**, with sketch → score, MIDI items → realisation, regions and take lanes → form and versions.
4. **The sketch file is the master copy, not the MIDI.** A band is one gesture; it can't be rebuilt reliably from dozens of notes. The Mac reads and writes the same file.
5. **Same feel on both devices.** The iPad is the sketchpad; the Mac is for full editing and writing MIDI. Gestures, terms, maths and file format must match, so that moving between them is seamless.
6. **Contribution, not "first".** Build on others' work and acknowledge it (section 11).

---

## 2. System overview

```
iPad sketchpad (web app, Apple Pencil, offline Home Screen app)
      │  Save → sketch file (.json) in iCloud Drive  ·  Export notes → .md for Obsidian
      ▼
Sketch file  =  master copy (strokes, envelopes, outlines, notes, annotations, field, shapes)
      │  Lua reads it (bundled JSON reader)
      ▼
REAPER Lua: LH Spectral Palette (Mac)  →  same canvas in gfx, full editing
      │  Commit  →  one MIDI item per layer, on child tracks in a folder, in a region, each commit a take lane
      ▼
LH synths (Breath, Additive, FM, Combs; later Prism and Modal)  or  any MIDI instrument
      │  Save back  →  sketch file  →  iPad again
```

**Toolkit MIDI convention (unchanged):** velocity × ADSR, **14-bit expression CC11 (MSB) + CC43 (LSB)** on each channel, **pitch bend on each channel, range ±24**, **Multichannel-8** output.

---

## 3. The iPad sketchpad as built (v14): full feature list

*Tested in a desktop browser at iPad Air 4 landscape size (1180 × 820) after each change. Real-iPad checks still needed: Pencil pressure and tilt, ⌘ + Pencil, the save dialog, the silent switch (see section 9).*

### 3.1 Canvas and field
- Log frequency **55 Hz–7.04 kHz** going up, **seconds** going across. **Duration** is set in m:ss or seconds, up to 20:00.
- **Changing the duration stretches or contracts the whole score**: units, splash timings, annotations and the play marker. Envelopes and outlines follow because they're relative. Unticking "Stretch the score with the duration" changes the length only. Undo restores both the duration and the material.
- **Field** lines to snap to: a harmonic series (partials 1–32), or stand-in chords (whole-tone, dominant 9th, Messiaen mode 2 chord, mode 2 full, quartal, open fifths) on roots A1, C2, D2, E2, F2 and G2. **These are to be replaced or extended by the ACCORD / LH_Accord presets.**
- A **Snap to field** toggle. With it off, bands are free regions following the drawn centre line.
- A **time ruler** under the canvas: tap or drag it to set the **play start** marker.

### 3.2 Layers (engines) and their drawn styles
| Layer | Engine | Hue | Drawn as |
|---|---|---|---|
| Breath | LH_Breath | slate blue `#4f6a8f` | glowing lines |
| Additive | LH_Additive_Texture_Synth | ochre `#b07d16` | crisp lines |
| FM | LH_FM_Texture_Synth_v2 | crimson `#a8323e` | lines with faint sidebands |
| Combs | LH_Sandstorm_Combs | moss `#577534` | blurred smears |
| Prism | *planned:* sine↔noise morph | indigo `#4b3f8f` | haze |
| Modal | *planned:* splash resonator | sienna `#9c4f2b` | crisp |

Bandwidth (sine → noise) is drawn as a haze around each line. Layers can be shown or hidden, and the toolbar dots choose which layer you draw on.

### 3.3 Tools (toolbar; keys B S V E H A)
- **Band:** a Pencil stroke draws a unit. **Pressure = loudness; tilt = bandwidth (sine ↔ noise).** It lights the field lines within its width around the stroke's centre line.
- **Splash:** a Pencil tap stamps a chord burst from the field, with attack, strum, decay, decay tilt (higher partials die sooner) and velocity (from pressure).
- **Select:** tap to select, drag to move, ⌥-drag to move a copy.
- **Erase:** tap or rub to remove units.
- **Shape (glissando editor):** four corner handles on the selected unit's outline. Notes keep their relative log position between the lower and upper edge, and the edges run straight from start to end, so the notes glide. Presets: Converge at end, Emerge from point, Fan out, Block. *Test version: handles move in pitch only.*
- **✎ Annotate:** Write (pressure-weighted ink), Arrow, Circle, Note (a pin, or a unit note if you tap a unit) and Erase. Annotations are graphite grey and make no sound.

### 3.4 Selecting and moving
- **The Pencil draws and fingers select:** a finger tap selects; a finger drag on the selected unit moves it. A resting palm (a long touch) is ignored.
- **A quick Pencil tap** selects instead of drawing.
- **Press and hold** a unit with the Pencil (about 450 ms) to pick it up and drag it.
- **⌘ + Pencil** selects in any tool and drags to move; **⌘⌥** moves a copy. ⌘ is also tracked from the keyboard, because the iPad may not pass it on with Pencil touches.
- Copy, cut, paste (at the last place you touched), duplicate, delete, and nudge with the arrow keys (0.1 s or a semitone; with ⇧, 1 s or an octave). Undo and redo hold 60 steps and include the duration and annotations. A tap that doesn't move anything adds no undo step.

### 3.5 Unit inspector (Settings panel)
- **Band:** width (oct), bandwidth (sine ↔ noise), tilt (dB/oct, dark ↔ bright), edge fade.
- **Splash:** width, attack, strum, decay, decay tilt, velocity.
- Layer reassignment, Delete, Duplicate, Copy, Paste, **Note** (add or edit), **Shape** presets.

### 3.6 Envelopes (Envelope panel; key 1)
- **Each unit has its own loudness envelope.** A chord has one envelope; any single note in it can **override** it with its own (marked ● in the menu).
- **Stored relative to the unit's length,** so it **stretches with the unit**. Loudness only, for now.
- **60 dB scale:** 1 = 0 dB, 0.5 = −30 dB, 0 = −60 dB (silent). The lane is labelled 0 to −60 in 12 dB steps.
- **The lane is zoomed to the unit** (from its start to its end), with a time grid and bold start and end times. Its height can be resized.
- **Editing:**
  - **tap the curve** to add a point, and keep dragging to place it
  - **double-tap a point** (or tap it, then ⌫ or **Delete point**) to delete it; the two ends always stay
  - **drag points** to move them
  - **tap between points** to pick a segment, then **drag its ◇** up or down to bend it
  - **draw freehand** starting away from the curve to replace that section; it's simplified to points
- **Curves for each segment:** Linear, **Exponential** (slow start, fast end), Logarithmic (fast start, slow end), S-curve, Smooth (monotone spline), Hold. **Tension** applies to Exponential and Logarithmic. **The default curve for new points is Exponential**, chosen under "New points" and remembered.
- **Loop unit (L):** solos the unit, or only the chosen note, on a loop.
- **● Record (R):** the unit plays once while you ride an on-screen **fader**. The envelope fills in live and is thinned to points. Stopping early leaves the rest unchanged.
- **Reduce points…:** a slider from the current number of points down to 2, removing the least important points first. The ends stay. Done or Cancel.
- **Shapes library:** Flat, Swell, Fade in, Fade out, Exp rise, Exp decay, Gust, Breath, Tremolo, Pluck, plus **your own** (Save shape…, delete with ×). Tap a shape to load it. Shapes are saved with sketches.
- **Copy and paste an envelope between units** (⌥⌘C / ⌥⌘V). It stretches to fit the new unit.

### 3.7 Playback (preview only)
- A sine or "organ" (additive) preview, while drawing and on Play. **Bandwidth and engine colour are heard only on the Mac.**
- **Play starts from the start marker.** Sounds already under way at that point join in part-way through. If the iPad pauses its audio, the playhead keeps time from the wall clock and a message explains why.
- Loop unit and Record, as above.

### 3.8 Notes and annotation
- **Score notes** (Settings), **unit notes** (a yellow comment icon at the unit's corner that moves with the unit), **pinned notes** (at a time and frequency), and **ink, arrows and circles** placed in score time.
- **Export notes for Obsidian (.md):** front matter (sketch name, file, date, duration, field, tags), score notes, unit notes in time order, pinned notes, and a count of drawn annotations.

### 3.9 Layout and saving
- **Slim one-line toolbar.** The canvas fills the window; **Envelope** (1) and **Settings** (2) panels open below and beside it, with **drag handles to resize**. **⤢** (F) tries full screen. **?** opens the in-app help, with all gestures and keys.
- **Save (⌘S)** writes the sketch .json (inside Claude: through the save dialog; otherwise a copy-text box). An **Unsaved / Saved hh:mm** indicator; a **reminder after 10 minutes** of unsaved work; **Save first / Don't save / Cancel** before New or Open. Work is also kept on the device as you go.

### 3.10 Keyboard (iPad keyboard, and the Mac)
| Keys | Action |
|---|---|
| B S V E H A | Band, Splash, Select, Erase, Shape, Annotate |
| ⌘C ⌘X ⌘V ⌘D | copy, cut, paste, duplicate a unit |
| ⌥⌘C ⌥⌘V | copy, paste just the envelope |
| ⌫ | delete the selected envelope point, otherwise the unit |
| ⌘Z ⇧⌘Z | undo, redo |
| ← → ↑ ↓ (⇧) | move in time 0.1 s (1 s), pitch a semitone (an octave) |
| N | note for the selected unit |
| Space · L · R | play, loop the unit, record its envelope |
| , . (⇧) · Return | move the play start 1 s (10 s), back to 0:00 |
| 1 · 2 · F · ? | Envelope panel, Settings panel, full screen, help |
| ⌘S · Esc | save, close or deselect |

---

## 4. Sketch file format, version 1

`format: "lh-spectral-palette-sketch"`, `version: 1`. All times in **seconds**, all frequencies in **Hz**. A full example is in `ipad/example_sketch.json`.

```jsonc
{
  "format": "lh-spectral-palette-sketch", "version": 1,
  "name": "…", "created": "ISO date", "modified": "ISO date",
  "time_unit": "seconds", "length_s": 60, "play_from_s": 0, "freq_range_hz": [55, 7040],
  "field": { "type": "harmonic|wholetone|dom9|m2chord|m2mode|quartal|fifths", "root_midi": 36, "root_hz": 65.406,
             "snap": true, "partials_hz": [ … ] },
  "layers": [ { "id": "breath", "name": "Breath", "engine": "LH_Breath", "hue": "#4f6a8f", "visible": true, "planned": false }, … ],
  "point_format": ["time_s", "freq_hz", "pressure_0_1", "tilt_0_1"],
  "strokes": [
    { "id": "…", "kind": "band", "layer": "breath",
      "params": { "width_oct": 1.6, "bandwidth": 0.35, "tilt_db_oct": -3, "edge_fade": 0.3 },
      "points": [[t, f, pressure, tilt], …],                 // the drawn centre line
      "env":  [[u, v, curve, tension], …],                    // optional; u 0–1 across the unit, v 0–1 on the 60 dB scale
      "note_env": { "196.22": [[u, v, curve, tension], …] },  // optional per-note overrides, keyed by partial Hz
      "shape": { "base_hz": [lo, hi], "left_hz": [lo, hi], "right_hz": [lo, hi] },  // optional glissando outline
      "note": "text" },                                       // optional unit note
    { "id": "…", "kind": "splash", "layer": "additive", "t_s": 12, "f_hz": 700,
      "params": { "width_oct": 1.8, "attack_s": 0.01, "strum_s": 0.25, "decay_s": 4.5, "decay_tilt": 0.7, "velocity": 0.85 },
      "env": …, "note_env": …, "shape": …, "note": … }
  ],
  "shape_library": [ { "name": "Windy", "pts": [[u, v, curve, tension], …] } ],
  "score_notes": "text",
  "annotations": [ { "kind": "ink", "pts": [[t, f, weight], …] }, { "kind": "arrow", "a": [t, f], "b": [t, f] },
                   { "kind": "circle", "a": [t, f], "b": [t, f] }, { "kind": "note", "t": 41, "f": 1500, "text": "…" } ]
}
```

- **Curve keys:** `lin`, `exp`, `log`, `s`, `smooth`, `hold`. A point's curve shapes the segment to the next point. A missing curve means `lin`; a missing tension means 0.5.
- The file also carries self-describing text fields: `envelope_format`, `envelope_curves` (with REAPER CC-shape hints), `outline_format` and `annotation_format`.
- **Keep the format backward compatible:** add fields, never rename them. Bump `version` only for breaking changes.

---

## 5. Maths the Mac version must match exactly

The full code is in `reference_core_maths.js`. In summary:

- **Frequency axis:** log, 55–7040 Hz. `mtof(m) = 440·2^((m−69)/12)`.
- **Which partials a band lights:** for field line `fp` and stroke point `(f, pressure)`, `d = |log2(fp/f)|`, `half = width/2`. The weight is 0 if `d > half`. Otherwise, apply a smoothstep edge over the last `edge_fade·half`, multiply by tilt `10^(tilt·log2(fp/f)/20)` and by pressure, and cap at 1.5.
- **Bandwidth at a point:** `bw = clamp(bandwidth·(0.4 + 1.2·tilt), 0, 1)`.
- **Splash timing:** the lit partials sorted low to high. Partial `j` starts at `t + strum·j/(n−1)`, and its decay is `decay·2^(−decay_tilt·log2(f/f_lowest))`. Amplitude: a linear attack, then `exp(−4.6·t/decay)`.
- **Unit span:** band = minimum to maximum point time. Splash = `t_s` to the latest partial's `start + attack + 1.2·decay`.
- **Envelope gain (60 dB):** `gain = 10^((v−1)·3)`, and `v ≤ 0.002` → silent.
- **Curves:**
  - **exp / log:** `t = 0.5 + 9·tension`, `e(x) = (e^{t·x} − 1)/(e^t − 1)`; exp uses `e(k)`, log uses `1 − e(1−k)`.
  - **S-curve:** smoothstep.
  - **Smooth:** cubic Hermite with monotone (harmonic-mean) tangents, flat at peaks and troughs, clamped to 0–1.
  - **Hold:** a step.
- **Glissando outline (warp):** `r = (ln f − ln base_lo)/(ln base_hi − ln base_lo)`. The lower and upper edges interpolate in log frequency from left to right across `u`, giving `f' = exp(lo(u) + (hi(u) − lo(u))·r)`. A single note uses a quarter-octave base around it.
- **Thinning:** freehand and recordings use Ramer–Douglas–Peucker in lane pixels (2.5 px and 1.5 px). Reduce points uses Visvalingam–Whyatt (smallest triangle area first).

---

## 6. The Mac (REAPER Lua) plan

### 6.1 First, check what exists (with Remote Control on, so Claude can read the folder)
1. **`LH_Spectral_Band_MIDI_GUI`:** the overview suggested the Palette might be its v2. Decide whether to extend it or write a new `LH_Spectral_Palette.lua`.
2. **LH UPIC MIDI:** how it does shapes and glissandi, the handle layout and channel allocation. **Match the iPad Shape tool to it**, and add time handles if the Mac has them.
3. **How the existing scripts write 14-bit CC11/43 and pitch bend:** point density, MSB/LSB order, how the ±24 range is set.
4. **ACCORD / LH_Accord:** the chord types and tunings (Debussy, Messiaen), to replace the stand-in chord fields.
5. **Craft and Drift:** the envelope-design tools, to keep the envelope behaviour consistent and plan their iPad equivalents.

### 6.2 Script structure
- **Lua `gfx` canvas** mirroring the iPad: the same axes, layer hues and drawn styles, the same envelope lane and the same gestures (mouse or trackpad for the Pencil; ⌘-click to select; ⌥-drag to copy).
- **A bundled pure-Lua JSON reader** (for example rxi/json.lua, MIT licence; credit it).
- **Open sketch:** a file chooser, plus a watched folder in iCloud Drive (for example `iCloud Drive/LH Palette/`) for sketches arriving from the iPad.
- **Region-based sketching** (from the overview): a sketch opens on a REAPER region, and the canvas becomes that window. Seconds stay the time unit (bars and beats were never decided).

### 6.3 Commit to MIDI (the high-fidelity goal: long fades, smooth glissandi)
- **One MIDI item per layer**, on child tracks inside a folder track (for example "Palette – Section B"). **Each commit is a new take lane** (REAPER 7).
- **One note per channel**, so each gliding note has its own pitch bend. That means **8 independent gliding voices per track** (Multichannel-8). Parallel-moving partials may share a channel. Spread denser chords across extra tracks.
- **Loudness:** 14-bit **CC11 + CC43**, calculated from the 60 dB envelope × pressure × band weight. Steps are about 0.004 dB. Write points densely during change (target error under 0.1 dB) and sparsely where nothing changes.
- **Glissandi:** 14-bit **pitch bend**, ±24 semitones (about 0.3 cent per step), target error under 0.5 cent.
- **Explicit dense 14-bit points are preferred** over REAPER's CC curve shapes, so the result is identical in every synth. The curve shape names are in the file if a lighter version is wanted.
- **Bandwidth and tilt:** to the synths that use them, as CC or FX automation (for example LH_Breath bandwidth).
- **Destination profiles** (proposed): "LH synths", "Sampler (ReaSamplOmatic5000)", "General MIDI". Each states the bend range, 14-bit or 7-bit expression, the channel layout, and what to do with parameters the receiver doesn't use.
- **Tagging:** items record the sketch id and a fingerprint of their contents. **Loading back:** if the MIDI is unchanged, the sketch reloads exactly. If it was edited in REAPER, those notes come in as a separate **raw-notes layer**.

### 6.4 Notes and annotations on the Mac
- Unit notes → **item notes** (`P_NOTES`). Pinned notes → **project markers** (or region names). Score notes → **project notes**.
- Ink, arrows and circles are drawn on the Lua canvas from the file, and saved back unchanged.
- Notes exported to Obsidian go to the same vault as the rest of the research.

### 6.5 Save back
- Write the same JSON (version 1) so the sketch can go back to the iPad. Keep any fields the Mac doesn't use.

---

## 7. Back to the iPad: offline Home Screen app

1. **Turn the page into an installable offline web app:**
   - add a web app manifest (name, icons, `display: standalone`, landscape)
   - add a service worker that caches the page and its fonts
   - add apple-touch icons
   - make **Save** work outside Claude: the iPad Share sheet ("Save to Files") and download links instead of Claude's save dialog, keeping the copy-text fallback
2. **Host it on Cloudflare Pages** (you have an account):
   - Workers & Pages › Create › Pages › Upload assets
   - project name, for example `lh-palette`
   - optionally a custom subdomain, and **Cloudflare Access** to make it private
3. **On the iPad,** open the address in **Safari** and choose **Share › Add to Home Screen**. Test in **Airplane Mode**: drawing, envelopes, Save to Files and reopening.
4. **Updates:** upload the new folder (or a zip) to the same project, then open the app once while online. To automate this, connect Cloudflare Pages to a GitHub repository, or give the Claude environment a Cloudflare token.
5. **Sketches:** save to an **iCloud Drive** folder that the Mac script watches. They're kept on the iPad while you're offline and sync when you're back online.

---

## 8. Backlog (discussed, not yet built)

- **Shape editor:** match it to UPIC MIDI; add time handles (start and end corners); curved edges.
- **Multi-select** (box or ⌘A) and group moves.
- **A Solo button** in the toolbar (play the selected unit once), and **layer solo** in Settings.
- **Spatial drawing:** 8-channel position per unit, or drawn trajectories (see Trajectoires and Smalley's spatiomorphology).
- **Morph lane** (crossfading engines) and **Transform** (transpose, stretch, rotate, range scale), from the overview.
- **Spectromorphological shape presets** named after Smalley's processes (dilation, contraction, convergence, divergence, accumulation, dissipation…).
- **Synths:** LH_Prism (sine → narrow band → wide noise as one dial, after Serra's sinusoids-plus-noise), the modal splash resonator, an FFT freeze/blur/chord-mask effect.
- **Sandstorm chordal combs** as an engine: wind (filtered noise) into five chord-tuned comb filters, gust-driven blooms, a tone/noise balance (see the 09 audio examples).
- **iPad equivalents of other Lua tools:** **LH MIDI UPIC** (agreed next), Craft and Drift (envelope design), tap-timing tools.
- **Score export** as PDF or SVG for performers, publication and papers.
- **A richer iPad preview** (a hint of the noise bandwidth), still light enough for travel.

---

## 9. Still to verify on the real iPad

- Pencil **pressure and tilt** values feel right; **palm rejection**; **press and hold** timing.
- Whether **⌘ + Pencil** reaches the page; if not, rely on press and hold.
- The **save dialog** inside Claude ("Save to Files").
- Audio with the **silent switch**, and the playhead message when the iPad pauses audio.
- **Full screen** (expected to be blocked inside Claude; it works as a Home Screen app).
- Portrait use: the toolbar scrolls sideways. Landscape is recommended.

---

## 10. From UPIC (to complete in the user's words)

The user worked at **Les Ateliers UPIC in Paris in the 1990s**. Concepts to decide on deliberately:
- **Pages and their sequencing** versus one timeline.
- **Banks:** separate libraries of waveforms and envelopes assigned to arcs. The shape library is a first step.
- **Playing a page live**, in real time.
- What was missed after UPIC, and what was only a hardware limit of its time.

*What we're recovering:* drawing and thinking spectro-spatially.

---

## 11. Precedents and acknowledgements (for the paper; TENOR, NIME, ICMC, *Organised Sound*)

- **Iannis Xenakis and the UPIC** (CEMAMu; Les Ateliers UPIC, later the Centre Iannis Xenakis). Lohner (1986), "The UPIC system: a user's report", *Computer Music Journal* 10(4).
- **UPISketch** (Centre Iannis Xenakis): iPad, inspired by UPIC. **HighC** (Thomas Baudel): desktop, structured additive curve objects.
- **Denis Smalley:** spectromorphology (1997, *Organised Sound* 2(2)) and spatiomorphology. **Manuella Blackburn:** visual sound-shapes. **Cat Hope:** animated graphic notation (Decibel ScorePlayer).
- **IanniX**; **Trajectoires** (Garcia, Favory and Bresson, 2016: iPad spatial trajectories over OSC); IRCAM ASAP apps; INScore.
- **Techniques:** Chowning (FM); Serra (sinusoids plus noise); Ramer–Douglas–Peucker and Visvalingam–Whyatt (line simplification); Fritsch–Carlson (monotone curves).
- **AI disclosure:** developed with Claude (Anthropic) from the user's designs and under his direction. The session transcript records where the design came from. Check each venue's policy and the university's.
- **Framing:** "a contribution building on…", never "the first".

---

## 12. How to work from here

1. On the Mac, unzip this package into **home** (it makes one `LH_Palette_Handoff` folder).
2. In the Claude desktop app: **Settings › Claude Code › Remote Control** → add **home**, or your toolkit folder.
3. Start Claude Code in that folder and say: *"Read LH_Palette_Handoff/HANDOFF.md, then look at LH_Spectral_Band_MIDI_GUI and LH UPIC MIDI and tell me which route fits (section 6.1) before building."*
4. Build order suggested in the overview, updated:
   1. Region commit and load back in REAPER
   2. Envelope lane parity
   3. Shape and glissando matched to UPIC MIDI
   4. Notes mapping
   5. The offline iPad build
   6. Morph lanes
   7. Prism, Modal and FFT

---

## v15 (3 Nov 2026): small, safe step for Mac ↔ iPad files

`ipad/lh-spectral-palette-sketchpad-v15.html`. v14 is unchanged next to it.

- **The problem in v14:** opening a Mac Score Tool sketch silently **dropped** blocks, lines, clouds, pulses, the Mac-only layers and Mac fields. Saving would then remove them from the file.
- **What v15 changes:**
  - Those units, layers, the `mac` block and a Mac-only field are kept untouched and written back on Save.
  - Mac-only units show as faint dashed outlines labelled "(Mac)"; they can't be edited on the iPad.
  - The Open message says how many were kept.
  - Also added: `<meta charset="utf-8">` (symbols were garbled when the page was served as a plain file) and a test hook, `window.__lh`.
- **Tested** in a desktop browser at 1180×820 with a band plus a Mac block, line and pulse: the band stays editable, the three Mac units are drawn as outlines, Save returns all four (the pulse byte-identical), and the layers and `mac` block survive.
- **Published (3 Nov 2026)** to the same link: https://claude.ai/artifact/UdUbHCZmrfRipnk4qcpvz9 (artifact version 15).
- **Next:**
  - the real-iPad checks in section 9;
  - the round trips: iPad → Mac (save on the iPad, open in the Score Tool, Hear) and Mac → iPad (save a Mac sketch, open it on the iPad, check the outlines, save, reopen on the Mac).

## v16 (3 Nov 2026): step 1 of matching the Mac

`ipad/lh-spectral-palette-sketchpad-v16.html`, published to the same link (artifact version 16).

- **Splash is shown as Impulse** everywhere you see it: the toolbar, help, messages and the envelope lane. The key is **I** (S still works). The file still says `splash`.
- **✥ Select / move** toggle in the toolbar, plus the key **S** (the user's choice, under the left hand; M also works). Impulse is **I** only. It switches the Pencil and trackpad between drawing and selecting / moving units, and goes back to the last drawing tool. ⌘ held and press-and-hold still work.
- **A 4 px threshold** before a drag moves a unit, so a tap only selects (as on the Mac).
- **Next (step 2):** blocks (chords) drawn, moved and heard on the iPad.

## v17 (4 Nov 2026): step 2, Blocks

`ipad/lh-spectral-palette-sketchpad-v17.html`, published to the same link (artifact version 18).

- **Block tool (key K):** drag a rectangle with the Pencil. The field lines inside it become the notes (up to 16); with Snap off, up to 4 semitone-spaced notes.
- **Matches the Mac's file format:** `kind: 'block'`, `t_s`, `dur_s`, `notes_hz`, `params {entry, arp_s, velocity, seed}`, plus the Mac's default exponential envelope.
- **Entry modes** as in the Mac's `Model.block_offsets`: chord, up, down, random (the same seeded generator, so Mac and iPad give the same order), fan out, fan in, strum. Entry, Arp step and Velocity are in the inspector.
- **Works like other units:** move, the S toggle, nudge, copy and paste, score stretching, envelopes (whole block or per note), outline shapes, and Play / Loop / Record.
- **Mac blocks open natively** if they are on an iPad layer. A block on a Mac-only layer (e.g. `texture`) stays a "(Mac)" outline.
- **Tested** in a desktop browser at 1180×820 (simulated Pencil): draw, move, entry, play, and the Mac round trip all worked with no errors. **Not yet tried on the real iPad.**
- **Next (step 3):** pulses (gap in ms, partials).

## v18 (4 Nov 2026): step 3, Pulses

`ipad/lh-spectral-palette-sketchpad-v18.html`, published to the same link (artifact version 19).

- **Pulse tool (key P):** drag across time with the Pencil. The pitch comes from the start (snapped to the field when it is within 1.2 st); ending more than 6 px higher or lower makes a glide (`f_end_hz`).
- **The Mac's model**, ported from `lhs_model.lua`:
  - `pulse_times`: rate from rate_hz to rate_end_hz with rate_curve, seeded jitter, or `taps`;
  - `pulse_freq`;
  - `partial_ratios`, the same languages (harmonic … chords … field);
  - `pulse_voices`: duty, accent every n, velocity jitter (seed + 7), partial tilt.
- **Checked:** a 4 s pulse at 4 Hz gives 16 pulses × 3 partials = 48 notes, the same as the Mac.
- **Settings:**
  - **Start gap / End gap in ms** (stored as Hz; gap = 1000 / Hz);
  - Rate curve, Length (duty), Jitter, Accent every, Partials, Partial tilt, Velocity;
  - a **Partials language** menu.
  - No outline presets for pulses (the Mac has none).
- **Tapped rhythms** from the Mac play and survive saving. Tapping on the iPad is not built yet.
- **Preview:** up to 260 voices now (was 140), for dense pulse trains.
- **Tested** in a desktop browser at 1180×820 with a simulated Pencil, with no errors. **Not yet tried on the real iPad.**
- **Next (step 4):** lines and clouds.

## v19 (4 Nov 2026): step 4, Lines and Clouds

`ipad/lh-spectral-palette-sketchpad-v19.html`, published to the same link (artifact version 20).

- **Line tool (key U):** draw freehand. The stroke is thinned (RDP 1.5 px) to `points: [[t_s, hz]]`; one voice glides in log frequency through the points, under its envelope; velocity in the inspector.
- **Cloud tool (key C):** drag a rectangle to get `edges {lo, hi}` as `[[u, hz]]`.
  - Ported from the Mac: `cloud_events` (the same seeded sequence), density shapes, note fade (exp curve, tension 0.4), "Notes glide with the edges", "Snap notes to the field", and a **New random seed** button.
  - **Checked:** seed 12345 (0–4 s, 200–800 Hz, density 6) gives 18 notes on both the iPad and the Mac.
- **The Mac layers Gesture, Texture and Clouds are added** to the iPad, so Mac lines, blocks and clouds open natively. Modal's engine now reads `LH_Modal`.
- **Not yet:** editing line points, or cloud edge points, by handle (the Mac has both).
- **Tested** in a desktop browser at 1180×820 with a simulated Pencil, with no errors. **Not yet tried on the real iPad.**
- **Next (step 5):** layers panel (Background all, ⌘-select layers).

## v20 (4 Nov 2026): layer button and step 5, the layers panel

`ipad/lh-spectral-palette-sketchpad-v20.html`, published to the same link (artifact version 21).

- **Toolbar:** the row of layer colour dots is now one button showing the current layer (colour + name ▾), at the user's request, to save space. It opens a list of the layers (marked background / hidden / muted); picking one closes it. Esc or a tap outside also closes it.
- **Layer views, as on the Mac:**
  - each layer is **full ● / faded into the background ◐ / hidden ○**;
  - the layer you draw on is always shown full and drawn on top;
  - faded layers draw at 28 % and can't be selected.
- **Settings › Layers:** **Background all** and **Show all**; per row, the view button and **M** (mute: silent when you Play).
- **Saved** as `layers[].view`, `.mute` and `.visible`, which the Mac reads. Mac files with `view` / `mute` (or the old `visible: false`) load correctly.
- **Tested** in a desktop browser at 1180×820, with no errors. **Not yet tried on the real iPad.**
- **Next (step 6):** envelope extras: LFO on a section, the simple LFO.

## v21 (4 Nov 2026): step 6, the LFO and LFO on a section
- **LFO button** (lane header): adds the Mac's default LFO (a sine, 4 cycles, ±9 dB, riding the drawn envelope, whole unit). Tapping it again shows or hides the LFO strip. The button reads "LFO ~" when the unit has one.
- **Simple strip:** Shape, Cycles (or Rate in Hz), Depth, the section readout, Whole unit, More ▸, Remove.
- **More ▸:**
  - Apply to the drawn envelope (ride), or a fixed Baseline;
  - Rate: cycles/Hz (switching keeps the speed);
  - Phase, Freq skew, Amp skew;
  - Tilt (sine, triangle) or Width (square);
  - Soft edges (when the LFO has a section);
  - New random seed (random shapes);
  - Presets… (the Mac's 10 built-ins);
  - Bake (into envelope points, about 0.6 px RDP, as Mac `bake_lfo`);
  - Less ◂.
- **Section:** tap **Section**, then drag across the lane; ⇧-drag works with a keyboard. If there's no LFO this adds one on that section, otherwise it moves the LFO there. Plum [ ] tabs at the foot of the lane drag the edges. The section shows as a plum band.
- **What you hear:** the lane shows the heard curve (LFO included) as a thin plum line over the fill. The editable points stay the drawn envelope.
- **Maths:** identical to Mac `Model.lfo_offset_db` / `env_fn`, including `env_mod` (offset_db / depth) from Mac files. `hash_rnd` is ported with `Math.imul` (the low 31 bits are exact). Checked against the Mac lib in REAPER: 12 of 12 values match (random, sine with skews and tilt, random smooth in Hz).
- **Code:**
  - `unitEnv` / `noteEnv` now return `{m, p, span}` when a unit has an LFO or env_mod, and `envAt` evaluates both forms;
  - `rawUnitEnv` / `rawNoteEnv` give the editable points (`targetEnv` uses them);
  - `heardEnv(s)` is used for the lane.
- **Shapes:** saved shapes keep their LFO, and applying one sets or clears the LFO (as the Mac). Built-ins leave the LFO alone.
- **Reset:** also removes the LFO and env_mod.
- **Fixed:** the Reduce points box and the shape-name box showed all the time (`display` overrode `[hidden]`).
- **Next (step 7, proposed):** line-point and cloud-edge handles, then iPad tap-rhythm for pulses, then an offline Home Screen build.

## v22 (4 Nov 2026): step 7, line-point and cloud-edge handles
- With a line or cloud selected and **Shape (H)** or **Select** active, its points show as handles, as on the Mac (`handles_of`: line_pt / line_mid / edge_pt / edge_mid).
- **Drag a point:**
  - a line point stays between its neighbours in time; its pitch snaps to the field within 0.6 semitones (hold ⌘ for free pitch);
  - an interior cloud-edge point moves in time and pitch; the end points move in pitch only.
- **⊕ midpoints** (shown when a segment is wider than 44 px): drag one to add a point there.
- **Double-tap or ⌥-tap a point** to remove it. A line keeps at least 2 points; a cloud edge keeps its end points.
- **Shape only:** drag a cloud's edge line, away from the handles, to move the whole edge (`edge_line`, scaled in log pitch).
- Finger, Pencil and trackpad all work. Each drag is one undo step, and a tap with no movement adds none.
- **Code:** `ptHandleTools`, `ptHandles`, `nearEdgeLine`, `handleAt` (returns corner handles or point handles), `startPtHandle`, `movePtHandle`, `ptDrag`, `snapNear`. The test hook gains `X` / `Y`.
- **Tested** with synthetic Pencil events: add, move and remove a line point; add a cloud-edge point; move a whole edge; undo.
- **Next (step 8, proposed):** tap rhythm for pulses on the iPad; then the offline Home Screen build.

## v23 (4 Nov 2026): no auto-play; ▶ Unit; no selection highlight
- **No auto-play:** a newly placed unit (block, pulse, line, cloud, impulse) no longer plays by itself, and handle edits don't either; the user wants to edit first. Band drawing still sounds live while drawing if "Hear while drawing" (Settings) is on.
- **▶ Unit** (toolbar, before ▶ Play) and **⇧Space:** play just the selected unit once; press again to stop. The button is disabled when nothing is selected. Space stops this and plays the score. Code: `playSelUnit`, `stopUnitPlay`, `unitPlay`.
- **No highlight:** the page no longer gets iOS text-selection or callout highlights (`user-select: none` on body; inputs, textareas and selects stay selectable). The score canvas and the lane have no focus outline.
- **Next: step 8**, tap rhythm for pulses on the iPad.

## v24 (4 Nov 2026): step 8, tap a pulse rhythm
- **Settings › selected pulse › ● Tap a rhythm…** opens a big TAP pad. Tap it with a finger, the Pencil or the trackpad (pointerdown, so there's no tap delay), or press **T**. Each tap gives a short tick at the pulse's pitch. **Done** (or Return) keeps the rhythm; **Cancel** (or Esc) discards it.
- Same maths as Mac `app.tap_finish`:
  - `u.taps` = (t − first) / dur;
  - dur = span + the average gap (room for the last pulse);
  - `u.dur_s` = dur, and `t_s` is unchanged.
- At least 2 taps are needed. Stretching the unit compresses or expands the rhythm (the taps are relative).
- **Use the rate again** removes `taps`. A note says the rate sliders are ignored while the unit follows taps. The canvas already labels it "tapped".
- **Code:** `tapRec`, `tapHit`, `tapFinish`, `tapClick`. The tap keys are checked before Escape and Return in the keydown handler.
- **Tested:** 5 taps (4 on the pad, 1 by T, with a fake clock) gave taps [0, .16, .32, .64, .8] and dur 1.563 s, as expected. Forget works.
- **Next (proposed):** an offline Home Screen build, then the Sketch Arranger.

## v25 (4 Nov 2026): annotations belong to the score
- **New:** now clears the annotations (ink, arrows, circles, pins) and the score notes along with the units. It also closes an open note editor and cancels tapping. Undo brings everything back: undo snapshots now hold `N` (the score notes) as well as `A` (the annotations).
- **Open…:** replaces the annotations with the opened file's, as before (`fromJSON`), and now also closes an open note editor.
- **Save:** annotations and score notes were already saved in the .json (`annotations`, `score_notes`) and in the iPad's local copy. Checked: save, New, then open restores them.
- **Mac:** already correct. `new_sketch` and `set_sketch` replace the whole sketch, and the saved file includes the annotations.

## v26 (4 Nov 2026): a pan envelope per unit (iPad first)
- **Lane:** a **Loudness | Pan** switch in the header. Pan mode edits `unit.pan_env` = [[u, pan 0..1 (0 left, 0.5 centre, 1 right), curve, tension]], with the same curves, shapes, copy/paste, reduce, freehand drawing and Reset (back to centre).
- The lane grid in pan mode reads R / R 50 / C / L 50 / L, and the fill is drawn from the centre line.
- In pan mode the note selector, LFO, Section and Record are disabled; pan is whole-unit only for now.
- **Sound:** `unitVoices` wraps `unitVoices0` and gives each voice a `pan` curve sampled from `pan_env` along the voice. `schedule` automates the voice's StereoPanner with it (plus ±0.12 of the usual voice spread). This applies to Play, ▶ Unit, Loop and impulses.
- **File:** `pan_format` is documented in the sketch JSON. The Mac keeps `pan_env` (normalize edits units in place), but the Mac doesn't use it yet.
- **Mac, to do:** a pan envelope in the Score Tool lane, and Commit writing per-channel CC10 (14-bit CC10/42?). Each LH synth also needs to read per-channel pan: Multichannel-8 → stereo position per channel. This links to the OM spatialisation port (4/8-channel).

## v27 (4 Nov 2026): per-layer iPad sounds (sound work, step 1)
- **Settings › Sound:** now **Layer sounds** (the default), Sine or Organ. In Layer sounds mode each voice's source follows its layer's engine (`ENGINE_SOUND`, `soundOf`, `buildSource`):
  - Breath / Clouds (LH_Breath): white noise through a band-pass at the pitch (Q 14), plus a quiet sine;
  - Additive / Texture: a 12-partial wave (1/k^1.25, even partials at 0.8);
  - FM / Gesture: a sine carrier and a 2:1 modulator, index 1.3, the modulation depth following the pitch;
  - Combs (LH_Sandstorm_Combs): noise through 5 band-pass "teeth" at 1–5 × f, Q 70. A Web Audio feedback delay can't go under 128 samples, so a real comb only works below about 345 Hz;
  - Modal: 4 sines at bar ratios 1, 2.756, 5.404, 8.933. The unit's envelope gives the decay;
  - Prism (planned engine): a sine plus a band of noise.
- Glides automate every frequency parameter (filters, modulator and its depth) as multiples of the voice's pitch, capped below Nyquist. Pan, loudness curves and the 260-voice limit are unchanged. The live drawing preview stays a sine.
- **Levels** (offline RMS at 440 Hz, amp 0.5): Additive .31, Modal .29, Combs .28, FM .26, Breath .24, Prism .24; Sine is .35. They're steady across 110–1760 Hz.
- The test hook gains `soundTest(layer, f)`, which renders one second offline. Scheduling the example score takes about 30 ms.
- **Next (sound step 2):** a shared presets file (`LH Sound Presets.json` in the iCloud LH Spectral Sketches folder): name, engine, slider values. Presets would be set per layer, then per unit; the Mac Commit sets the JSFX sliders and the iPad maps what it can. **Step 3:** exact AudioWorklet ports of the JSFX, one at a time.

## Reverted to v26 (4 Nov 2026)
- The user preferred the earlier pure-sine sound ("more sophisticated"; disliked the breathy noise layers). The published sketchpad is **v26 again** (artifact version 29). v27 is kept as `lh-spectral-palette-sketchpad-v27_layer_sounds_REJECTED.html` for reference only.
- **Lesson:** the per-partial pure sines are the point; they make the drawn spectrum audible exactly. Any later layer colouring should stay sine-based and subtle, with no noise sources: a Modal decay or slight inharmonicity, an FM shimmer, a Combs ring, a slow Breath movement. Ask before changing the default sound again.

## v28 (4 Nov 2026): first iPad sound preset, ported from REAPER
- **Settings › Sound:** Sine (still the default), Organ, or **Sine + REAPER presets**. In presets mode, layers with a preset use it and every other layer stays sine.
- **First preset:** `breath_gentle1`, "Gentle breathy sound 1". It's **LH Breath** as set on track 9 of *LH Score Tool – Workspace.RPP*, read live from REAPER:
  - bandwidth 1% (floor 0.5 Hz), Reson;
  - attack 4 ms, decay 3 s, sustain 70%, release 6 s, exponential to −60 dB;
  - spread 60%, even scatter, note width 40%, no drift, out −12 dB, pitch bend ±24.
  It's used for the **Breath layer only**.
- **Port** (from the LH_Breath.jsfx code):
  - uniform white noise into a band-pass (Web Audio RBJ biquad, Q = f / bw, the same 3 dB width as the JSFX TPT SVF), normalised to unit RMS with √(3·sr/(π·bw)), the same formula as the plug-in;
  - Note Width as a second independent band, mid/side L = m + s, R = m − s, with wth = width·π/4;
  - golden-ratio Even scatter × spread, and the plug-in's pan law (L·√(1−p), R·√p), automated by `pan_env`;
  - the ADSR on the plug-in's dB scale (times are floor to 0 dB) multiplies the unit's loudness curve, which acts as CC11, and a release tail is appended.
- **Measured** offline at 55 / 440 / 3520 Hz:
  - held level about −3 dB under sine (the sustain of 70%);
  - L/R correlation 0.80–0.86, against 0.81 expected;
  - the tail is −10 dB after about 1 s and about −38 dB after 4 s, as 60 dB over 6 s gives.
  Scheduling the score takes about 25 ms.
- **Code:**
  - `IPAD_PRESETS` (id, name, engine, from, layers, params with JSFX names); this is the start of the shared library format;
  - `presetFor`, `breathEnvelope`, `buildSource` (sine, or a stereo preset source);
  - `schedule` handles stereo sources with an L/R pan law;
  - test hook `presetTest(layer, f, secs)`.
- **Not yet:** Steep band shape, pitch and pan drift, per-unit presets, a shared presets file, and an iPad editor for preset settings.

## v29 (4 Nov 2026): Sound Lab, step 1 of the iPad synthesis environment
- **Opening it:** Settings › **♪ Sound Lab…**, or key **3**. Esc or Done closes it. It's a full-screen sheet with three parts:
  - **Presets list:** REAPER presets (built-in, read-only) and yours.
  - **Controls:** all of **LH Breath**'s controls, with the plug-in's names, ranges and defaults (`BREATH_DEFS` = JSFX sliders 1–19, without bend range or output mode):
    - Band: bandwidth (log), floor, Reson/Steep;
    - Envelope: attack, decay, sustain, release (log ms), Exponential/Linear, exp floor;
    - Movement: pitch drift, drift rate, pan drift;
    - Space: spread, pan layout (Random, By pitch, Alternate, Even scatter), note width;
    - Output: tune, output gain. −12 dB is the reference, mapped to the sine level.
  - **Pads:** the field's notes between 110 Hz × 2^oct and 8× that (up to 16), with Octave ± (−2..+3). Press and hold for attack, decay and sustain; let go for the release. **Hold chord** holds 4 field notes. **▶ Test phrase** plays two notes, a 3-note chord, and a glide up a fifth through `schedule`, the same path the score uses.
- **Editing a REAPER preset** automatically makes a copy, "<name> (iPad)", noting where it came from. Duplicate makes a copy; Delete (yours only) asks first. Renaming is done in the Name field.
- **Use in the score:** choose a layer, then **Use on this layer**. This sets `state.layerSound[layer] = id` and switches Sound to "Sine + Sound Lab presets". **Back to sine** removes it.
- **Storage:**
  - your presets are in localStorage `lh-ipad-sound-presets-v1`, and the per-layer choices in `lh-ipad-layer-sounds-v1`;
  - the sketch JSON gains `ipad_sounds` {mode, assign, presets used}, and `fromJSON` imports missing presets and the assignments.
- **Engine additions to the v28 port:**
  - Steep: 2 biquad stages, each widened by STEEP_W = 1/√(√2−1), with √(6·sr/(π·bws)) normalisation;
  - Tune, as a multiple of the frequency;
  - pitch drift: `wander()` (new target with chance rate·dt, one-pole at the rate), automated as the filters' detune;
  - pan drift: wander on the L/R pan law;
  - pan layouts as in `voice_on`;
  - linear/exponential `env_gain`, now normalised like the plug-in, (10^(dB/20) − f0)/(1 − f0);
  - output gain.
- **Tested in the browser:** opening; 14 sliders and 3 selects; editing a REAPER preset makes a copy (bandwidth 2.4% from the log slider); pad hold and release; chord; phrase; assign; Steep plus drift renders (corr 0.84); JSON round trip. No errors.
- **Next:**
  - **step 2:** the shared presets file in iCloud; the Mac Commit applies the preset to the JSFX;
  - **step 3:** more synths in the interactive session, Additive / FM / Modal / Spatial Sub (OM Sub-1); each needs an `ENGINE_DEFS` entry plus a `buildSource` branch.

## v30 (4 Nov 2026) — typed values + keyboard pads
- Every slider read-out (Settings inspector and Sound Lab) is tappable: type an exact number in the units shown, Enter/blur applies, Esc cancels. Values are clamped to the slider range but not snapped to its step. Inspector units are recovered from each def's `fmt` (`dispScale`: %, 0–127, ms gap → rate_hz = 1000/ms). Helpers: `parseNum`, `dispScale`, `numEntry`.
- Sound Lab + hardware keyboard: 1–0 then Q–Y play pads 1–16 (hold = sustain, key up = release; key label shown on each pad); − / = octave, Space test phrase, Esc closes. While the Lab is open all score shortcuts are swallowed (capture-phase handler, ⌘ shortcuts pass). Key 3 still opens the Lab from the score; inside it, 3 is a pad.

## v31 (4 Nov 2026) — Sound Lab: Additive, FM, Modal engines
- Ported from the JSFX code: LH Additive Texture Synth (one sine per partial; ratio (k+1)(1+inh·k²·0.001), detune spread, shimmer as slow per-partial level curves; one-pole attack/release), LH FM Texture Synth v2 (PM done as FM: modulator = PeriodicWave of the derivative of the feedback sine y=sin(φ+βy), × f·mod_ratio × index into carrier.frequency; index drift and ratio drift as curves; sub osc), LH Modal (mode tables, brightness/hardness levels, per-mode T60 with tilt, note-off damping, per-mode pan; strike = sines from zero phase with setTargetAtTime decays).
- Presets read from the REAPER preset banks (hex .ini decoded): Add 1–4, FM: 1, Slightly metallic (the two "Accord Detuner" ones were identical; the detuner was a separate plug-in), Fluttering 1, Rough modulating 1–3. Eight new LH Modal starters (bar, glass, bell, gamelan plate, membrane, plucked harmonic, stretched piano-like, long plate), gains set so strikes peak near sine level.
- Defs carry `s:` = plug-in slider number, for the Mac Commit (step 2).
- Level: all engines = plug-in output × 2√2 (same factor as Breath), so REAPER's balance between synths is kept. Heavy engines get a voice budget (900 oscillators, loudest first).
- Not ported (different kind of instrument — self-generating chord drones with gusts): LH Wind Organ, LH Sandstorm FM, LH Sandstorm Combs.
- Note: Add 1–4 all have Fundamental Ratio 0.34, so they sound ~18.7 semitones below the drawn pitch, as in REAPER.
- Code: `ADD_DEFS`, `FM_DEFS`, `MODAL_DEFS`, `MODAL_SETS`, `ENGINE_ORDER`, `ENGINES{hold, rel, relLen, holdLen, cost, source}`, `engineEnvelope`, `modalModes`, `fmModWave`; source `at(t0, hold, total, el)` / `off(t)` hooks; `__lh.sound(id)`; `presetTest` accepts a preset object and reports `strike`.

- v31.1: Add 1–4 now have Fundamental Ratio 1 on the iPad (REAPER presets still 0.34 — user asked for 1).

## v32 (4 Nov 2026) — iPad sounds reach REAPER; unit library
- iPad: each preset written into a sketch (`ipad_sounds.presets`) now carries `mac = {engine, sliders: {"slider number": value}}` (defs have `s:`; select controls map to the slider's index, Breath env_curve uses `map {exp:1, lin:0}`).
- Mac (Score Tool lib v1.7, lhs_commit.lua + lhs_app.lua; copies in `LH Score Tool/v1.7_2026-11-04`, pre-change backup in `LH Score Tool/backups`): `Commit.ipad_preset(sk, L)`; `Commit.engine_for(L, sk)` — a layer with an iPad sound uses that sound's synth; `apply_ipad_sound` sets the sliders after `setup_synth` on every Commit and Audition (the iPad sound wins over hand edits on those tracks). JSFX `:log` sliders take ln(value) in TrackFX_SetParam — read from the .jsfx file (`log_sliders`). Layer list shows "· iPad: <preset>".
- Verified in REAPER (scratch tab): Breath, Additive, FM, Modal sliders all equal the iPad preset after Commit and Audition.
- Unit library (iPad): Save to library (selected unit), Y opens the library: rename, ▶ Hear, Place (copy at cursor / play point), Delete. Stored on the iPad and in every sketch as `unit_library` (Mac keeps unknown fields, so it round-trips).
- Library file: `LH Library.json` (format `lh-spectral-library`: units + Sound Lab presets) — Export/Import in the Unit library (also via Lab › Library file…); the main Open also accepts it.
- Not yet: Mac → iPad (capture a REAPER synth's settings as an iPad preset); a Mac UI for the unit library.

## v33 (4 Nov 2026)
- Top strip: undo/redo buttons removed (user uses ⌘Z / ⇧⌘Z); ♪ Sound Lab button moved from Settings › Sound to the strip, between Envelope and Settings.

## v34 (4 Nov 2026)
- Sound Lab side panel: the four synth methods as buttons (Breath / Additive / FM / Modal); that synth's presets in one drop-down grouped From REAPER / Starters / Yours. Switching synth returns to the preset last used on it (`labLastByEngine`).

## v35 (4 Nov 2026) — Sound Lab preset files
- The Lab edits a working copy (`labWork`, `loadWork`, `labDirty`); pads / test phrase play the working copy; the score and layer assignments use the saved preset.
- Preset bar: name field + Save (own preset: overwrite incl. name; built-in: makes your own copy, the original stays), Save as new, Revert, Delete (own only; layers using it go back to sine). Names kept unique (`uniqueSoundName`).
- Switching synth / preset, closing the Lab, or opening the library with unsaved changes asks Save / Discard / Cancel (`labGuard`).
- `ask()` now shows inside the Sound Lab or Unit library sheet when one is open (fixes hidden confirms there, incl. unit-library Delete).
- Old auto-copy-on-edit (`editable()`) and the Duplicate button removed.

## v36 — Grouping in the score (2026-11-04)
Artifact version 39. File: `ipad/lh-spectral-palette-sketchpad-v36.html`.
- Multi-select: ⇧-click / ⇧-tap adds or removes a unit; marquee drag on empty score in the Select tool (V) or with ⌘ held; ⌘A selects all.
- ⌘G groups the selection (shared `group` id on each unit); ⇧⌘G ungroups. Clicking any member selects the whole group (rust outline "group · N").
- The whole selection moves, ⌥-drag copies, nudges, deletes, copies/pastes (clip is an array), duplicates (copies get new group ids), plays.
- Panel "N units selected": Group / Ungroup / Duplicate / Copy / Save to library / Delete; Reshape time ×½ ×0.9 ×1.1 ×2 (stretched about the selection start) and pitch −oct −1 +1 +oct.
- Unit library stores groups as `entry.units` ("Group of N"); placing one places every unit.
- Mac Score Tool keeps the `group` field but does not act on it yet.
- Tested in browser: marquee, ⌘G, click-selects-group, drag, ⇧-add/remove, duplicate, undo, stretch, transpose, copy/paste at cursor, library save, ungroup, delete — no console errors.

## v37 — Edge trim (2026-11-05)
Artifact version 40. Select tool (or ⌘, or finger on a selected unit): drag a unit's left/right edge.
- Plain drag = stretch: other end fixed, content (points, edges, shape, glide) rescales. Selection/group stretches as a whole.
- ⌥-drag = crop (grabbed unit only): content stays in time; shortening cuts, lengthening holds the end value. Envelopes stay relative (span the unit).
- Edge trim beats point handles unless within 10 px of the point. Splash has no edges.
- Fixed: ⌥-press without moving no longer leaves a stray copy.

## v38 — Chord unit (2026-11-05)
Artifact version 41. Modelled on Texture Seqs MIDI v2 (original). Stored as `kind:'block', chord:true` so Mac Commit already plays it as a block.
- Chord tool (O): drag across time → chord (bottom/top pitch rounded to semitones), opens in note edit.
- Edit notes (Enter / tap chord with Chord tool / panel button): tap column = add note on semitone grid (⌘ = free pitch), tap note = remove, drag note = move by semitones (⌥ = cents, ⌘ = free). Grid + note names drawn in the column. Esc/Enter = done.
- Panel: type notes (C3 E♭3 G3+14 · MIDI 60.5 · 440hz), Round to semitones, ▶ Hear; entry modes/velocity/envelope as block.
- Top/bottom handles (Select) stretch the spread (top keeps bass, bottom keeps top; rounded unless ⌘). Body drag transposes in semitones (⌘ free). Edge trim works.
- Fixed: annotation bar was always visible (CSS [hidden]).

## v38.1 (2026-11-05)
Settings: unit editing section now sits above Layers · engines.

## v39 — Settings: Unit | Score tabs (2026-11-05)
Artifact version 43. Unit = selected unit or next-one brush (+ multi-select/Reshape). Score = Sketch, Layers · engines, Field, Keyboard, This sketch. Selecting a unit or a drawing tool opens Unit; ⇧2 switches; 2 shows/hides the panel.

## v39.1 (2026-11-05)
Top strip: Settings button now between ▶ Play and Envelope.

## v40 — Notes on / off for Block and Impulse (2026-11-05)
Artifact version 45. Settings › Unit shows the notes as chips (tap = on/off, plays the note); ⌥-click a note on the score does the same. Off notes are faint dashed ghosts, silent. At least one note stays on.
- Block: off notes move to `notes_hz_off` (Mac plays `notes_hz` unchanged).
- Impulse: `notes_off` = Hz of switched-off partials, matched within 10 cents; follows transposes.
- Mac: `lhs_model.lua` splash_voices skips `notes_off` (copy in `LH Score Tool/v1.8_2026-11-05/`, backup in backups/). Syntax-checked in REAPER, not yet run on a Commit.

## v41 (2026-11-05)
Artifact version 46. Line: hold ⇧ while drawing = straight line from the start point. Pulse: hold ⇧ = flat (no glide); without ⇧ = straight glide as before.

## v42 — Pulse bend (2026-11-05)
Artifact version 47. Pulse gets `bend` = [[u, hz], ...] (u 0..1, endpoints included; f_hz / f_end_hz mirror the ends). Select/Shape: drag end points or bend points (snap to field, ⌘ free), ⊕ adds, double-tap/⌥-tap removes (back to a straight glide when only ends remain). Transpose, edge trim (stretch/crop) carry the bend.
- Mac (v1.8 copy in `LH Score Tool/v1.8_2026-11-05/`): `Model.pulse_freq` follows `bend`; transpose scales bend, impulse `notes_off`, block `notes_hz_off`; canvas draws the curved pitch path. Syntax-checked in REAPER, not run on a Commit yet. Mac has no bend-editing UI (parity list).

## v43 — Zoom time / pitch (2026-11-05)
Artifact version 48. `view {t0, t1, l0, l1}` drives X/Y/TofX/FofY; strokes clipped to the plot; grid shows semitone labels when zoomed past ~2.5 octaves, time steps down to 0.1 s.
- Two fingers: spread/pinch = zoom (⌥ = pitch only, ⌘ = time only, neither = both), move = pan. Trackpad pinch the same (gesture events or ctrl-wheel); two-finger scroll pans; ⌥/⌘-scroll zooms. 0 = whole score. View not saved in the sketch.
- Two-finger touch cancels a finger drag in progress (restored).

## v43.1 (2026-11-05)
Artifact version 49. Trackpad pinch inside the Claude app magnifies the page (the viewer takes it), so: ⌘ + two-finger scroll = zoom time, ⌥ + two-finger scroll = zoom pitch, ] [ / ⌥] ⌥[ keys, − + Fit buttons bottom-left of the score. Page-level gesture events are blocked/routed where the host lets them through. True pinch expected in the standalone build.

## v43.2 (2026-11-05)
Artifact version 50. User: ⌘/⌥ + two-finger scroll does not reach the sketchpad in the Claude app (on-screen buttons do). Added axis drags: time ruler up/down = zoom time (then sideways = scroll; plain sideways = play point); pitch labels either side up/down = scroll pitch, toward/away from the score = zoom pitch in/out.

## v43.3 (2026-11-05)
Artifact version 51. ] [ / ⌥] ⌥[ (confirmed working on iPad) and the − + buttons zoom about the cursor (pointer over the score, else the selected unit, else last touch) and centre it on screen. User zooms by keys or fingers only — not axis drags. Trackpad pinch is taken by the Claude app; on-glass two-finger pinch is in since v43 (untested by user).

## v43.4 (2026-11-05)
Artifact version 52. Removed the on-screen Time/Pitch − + Fit bar; zoom by keys only ( ] [ time, ⌥] ⌥[ pitch, 0 = whole score).

## v44 — layers per score (5 Nov 2026)
- Each score has its own layers: 4 to start (Breath, Additive, FM, Modal), "+ Add layer" for more. A layer = one sound = one REAPER track; units have no sound of their own.
- Score settings → layer row: colour dot (tap to pick), name (type, Enter), sound select (Sound Lab presets; picking one switches Sound mode to presets and sets the Mac engine), ●◐○ view, M mute, S solo, ✕ remove (only when the layer has no units).
- v44.1: layers are named Layer 1, 2, 3… (old engine names like Breath/FM are renamed on load); the row's sound select is labelled "Sound".
- Playback: audible = not muted and (no solo, or soloed).
- JSON: `layer_set: 2`; `layers` holds only this score's layers (with `solo`). Older files (all 9 catalogue layers listed) load as the layers in use or with a sound, topped up to 4.
- Mac `lhs_commit.lua`: reused tracks now take the layer's name and colour on re-commit; `I_SOLO` follows `solo`. Syntax-checked in REAPER, not yet run on a Commit.

## v45 — fields match the Mac (5 Nov 2026)
- iPad FIELDS now has every Mac `lhs_maths.lua` field, same ids: chromatic, qtone, etone, odd, subharm, stretch, compress, edo19/31/53, bp, Messiaen modes 3–7. EDO lines labelled note ± cents; undertones 1/n.

## v46 — Debussy / Messiaen / spectral fields (5 Nov 2026) — iPad + Mac
- New field ids (iPad FIELDS and Mac lhs_maths.lua M.FIELDS, identical maths, checked line-for-line): penta, acoustic, phrygian, aeolian, lydian; resonance, domchord, fourthsm (voiced chords, repeated every whole number of octaves above their span); distort (stretch param), fm (interval = carrier above root, ratio = mod/carrier, |c ± k·m| k ≤ 16), ring (interval = 2nd note, |i·f1 ± j·f2| i,j ≤ 4), bell (interval = bell pitch, 15 inharmonic ratios incl. hum 0.5), tworoots (harmonics 1–32 of root and root+interval), deepodd (odd partials of root / 2^octdown), edo72.
- Field settings saved in `field`: stretch, ratio, interval, octdown (defaults per field; interval resets on field change).
- iPad: Field menu grouped Main / Debussy / Messiaen / Spectral / Tunings; settings appear under the Field row. Mac: new fields under Additional fields; "Field settings…" in the Field menu (GetUserInputs). Mac syntax-checked in REAPER.
- "Chord of transposed inversions" replaced by Messiaen's chord in fourths (exact voicing of the former not verified).

## v47 — outline edge points for Band / Block / Impulse (5 Nov 2026)
- iPad now reads and writes the Mac's `shape.lo_pts` / `shape.hi_pts` ([[u, hz]]); warp uses them (same interpolation as lhs_maths `edge_log_at`). left_hz/right_hz kept equal to the end points.
- Shape tool: dashed outline through all points, corner + edge handles, ⊕ between points adds one, double-tap (or ⌥-tap) removes an inner point. Crop, transpose and the presets keep the points consistent.
- Fixes a silent bug: before v47 the iPad ignored lo_pts from Mac files and left them stale when corners were dragged.

## v48 — Arc unit (5 Nov 2026)
- Tool "Arc" (W). Drag start → end: an arch (apex ½ oct above the higher end); ⌥ while drawing = S-curve, ⇧ = ends level. Ends snap to the field (⌘ = free).
- Stored as an ordinary `line` (width 0 = one gliding tone) or `band` (width > 0) plus `arc: {u: [handle positions 0–1], band_width?}`. Points are a natural cubic spline in (time, log Hz) through the handles, resampled (32–160 pts) on every edit; handle pitches are read back from the points, so move / transpose / stretch keep the curve. Crop re-fits.
- Editing (Arc, Select or Shape tool): round handles = start / bend(s) / end; yellow ◆ = width (drag up to widen, down to 0 = tone). Panel: Tone ¼ ½ 1 2 3 oct chips + Width slider, Arch / S-curve / Flip ↕.
- Mac: plays and draws it already (it is a line / band with points; `arc` kept on save). Parity gap: Mac Arc tool + handle editing.

## v49 — Split (5 Nov 2026)
- `/` (or Split ✂ in the Unit panel) cuts the selected unit(s) at the pointer's time (last canvas position; else the play point). Right-hand pieces are selected; grouped units: left pieces keep the group, right pieces form a new one. Impulses don't split.
- v49.1: the Split ✂ button arms a cut (red ✂ line follows the pointer); the next click / tap on the score cuts there; Esc cancels.
- Each piece gets its share of env / pan_env / note_env (value at the cut interpolated), outline, arc, pulse bend (via cropUnit).
- Exact notes: cloud piece gets `fixed = {dur, ref, evs: [[t, d, f, r, v]]}` (times scale with length, pitch with the edges' geometric mean ÷ ref); any cloud setting change (except note fade), new seed or edge edit drops `fixed` (re-scatter). Pulse piece gets `taps` (its onsets) + `pulse_off` (accent / velocity-jitter sequence offset). Verified: split cloud = original within 0.05 ms / 0.02 cents; pulse identical.
- Mac `lhs_model.lua`: cloud_events honours `fixed`; pulse voices honour `pulse_off`. Syntax-checked. Parity gap: Mac Split command.

## Mac LH Score Tool v1.9 — parity pass (5 Nov 2026)
New `lhs_edit.lua` (arc spline, crop, split). Copies in `LH Score Tool/v1.9_2026-11-05/`.
- Arc tool (W): drag to draw; handles move points, ◆ sets width (0 = gliding tone); Inspector Tone/¼–3 width, Arch, S-curve, Flip.
- Split: `/` at the mouse, or right-click › Split here. Clouds keep notes (`fixed`), pulses keep taps (`pulse_off`), envelopes shared at the cut.
- Grouping ⌘G / ⇧⌘G; selecting one selects the group.
- ⌥ side handle = crop (lengthening allowed).
- Pulse bend points: drag, click line to add, ⌥-click to remove.
- Block edit: ⌥-click a note = off (dashed), click again = on.
- Layer menu: Custom colour…, Sound (Sound Lab preset) submenu; solo writes I_SOLO.
- Field settings… in the Field menu (stretch / ratio / interval / octaves down).
Checked: syntax + functional tests pass; GUI opens in REAPER without errors. Mouse paths not yet hand-tested.

## Mac LH Score Tool v2.0 — remaining parity (5 Nov 2026)
Copies in `LH Score Tool/v2.0_2026-11-05/`; backups `*_before_v2.0_2026-11-05.lua`.
- Chord tool (O): drag across time → `kind block, chord = true` (ends rounded to semitones), opens note edit. Column shows a semitone grid with names. Click = add (hears it), click a note = remove, drag a note = move (semitones; ⌥ cents; ⌃ free), ⌥-click = off. Chord tool on a chord = edit it. ▲▼ spread handles (top keeps bass, bottom keeps top; ⌃ free). Inspector: Round to semitones, ▶ Hear.
- Notes on/off: inspector chips for Block and Impulse; ⌥-click a note of the selected unit on the score. Off notes drawn dashed. At least one stays on.
- Inspector Unit | Score tabs (⇧2). Unit = selection, or the next-unit brush; Score = sketch, REAPER, generators.
- Unit library (Y, inspector, right-click › Save to library): Hear, Place at the play point, Rename, Delete; Import/Export `LH Library.json` (units + Sound Lab presets). Global file `REAPER/Data/LH Score Tool/LH Library.json`; also written into each saved sketch as `unit_library` and merged on open (same as the iPad).
- Fixed: ⌥-click without moving no longer leaves a stacked copy.
Checked: syntax + functional tests pass; GUI opens. Mouse paths not hand-tested.

## Mac LH Score Tool v2.0.1–2.1 (6 Nov 2026)
- Hide (H / Hide button) + running the Score action again toggles it (set_action_options 1|4); view and tool are restored (project ExtState view_<mode>). The Mac keeps script windows above REAPER's main window — js pin / SetParent / NOTOPMOST don't change it.
- Insert silence (⇧I, Score tab, right-click › Insert silence here…): at m:ss.ms, length s; units crossing the point split (Ed.split), everything later + annotations + play point move later, length grows. Tested: block 8–14 split at 10 → 8–10 + 12.5–16.5.
Copies in `LH Score Tool/v2.1_2026-11-06/`.

## v50 — Insert silence (6 Nov 2026) — iPad + Mac
Artifact version 62. Settings › Score › Insert silence (at m:ss.ms, length s, Insert / Enter); ⇧I fills it with the pointer time. Same rules as Mac v2.1: units crossing the point split (splitUnit), later units/annotations/play point move, Mac-only units shifted, length grows. Tested: band 1–27 at 20 + 2.5 → 1–20 + 22.5–29.5; undo restores.
Mac v2.1 also: view clamped at 0:00 (fit/zoom/scroll/zoom-to/restored view), moves and arrow nudges stop at 0:00.

## v50.1 (6 Nov 2026) — iPad + Mac
Artifact version 63. Insert silence asks only the length (user: no "at" field). iPad: Insert = at the play point, ⇧I = at the pointer with the panel's length. Mac: ⇧I = at the mouse, right-click › here, Score tab button = at the play point; dialog asks length only.

## v50.2 (6 Nov 2026) — iPad + Mac
Artifact version 64. Insert silence is a prompt on both, length as mm:ss:hh (00:02:50 = 2.5 s; plain seconds and m:ss.s also read). iPad: floating prompt (⇧I at the pointer, Settings › Score › Insert silence… at the play point). Mac: Mx.fmt_msh / Mx.parse_msh.

## v51 / Mac v2.2 — time selection + Remove time (6 Nov 2026)
Artifact version 65. ⇧-drag the time ruler = time selection (two lines + shade; drag a line on the ruler to adjust; snaps 0.01 s iPad / snap grid Mac). Remove time (iPad bar at the bottom · Mac right-click / Score tab · both ⇧⌫): split at both lines, delete units starting inside, shift later units/annotations/play point back, length shrinks. ⇧I with a selection = insert that length at the left line. Esc clears. Both tested with the same case: blocks 2–6, 8–14, 12–13, 13–23, 30–34, remove 10–15 → 2–6, 8–10, 10–18, 25–29.
Mac Save as… now starts in the folder the sketch came from (iPad sketch → iCloud folder). Copies in `LH Score Tool/v2.2_2026-11-06/`.

## v51.1 / Mac v2.2.1 (6 Nov 2026)
Artifact version 66. Envelope lane: ⌥-click / ⌥-tap (Pencil) a point = delete, on both (double-tap / double-click and ⌫ still work). First and last points stay.

## Parity — iPad ↔ Mac (goal set 2026-11-04; updated 5 Nov after Mac v2.0)
- To Mac: Sound Lab preset editing; typed slider values.
- To iPad: Wind Organ + Sandstorm sounds; Mac→iPad sound transfer (file).
- Both: offline/standalone iPad build + round-trip test session.

## iPad v52 / Mac v2.3 (6 Nov 2026): Obsidian export with stamps, key data and picture
- Notes are stamped when written or changed, as local "YYYY-MM-DD HH:MM": unit `note_at`, pin/annotation `at` (Mac unit pins `pins[].at`), sketch `score_notes_at`. Both sides keep the others' stamps.
- Export notes (.md): frontmatter (exported, created, duration, units, layers, source), **Key data** (length, units by kind, layers + sound, sounding span, pitch range, densest moment, three longest silences, note counts), **Score** = the whole score as an embedded JPEG data URI (one file), then score notes / unit notes / pins with stamps. File name carries the export date and time.
- iPad: `scoreImage()` renders off screen at 1100×480 @2x; `scoreFacts()`, `unitHz()`. Test hooks `__lh.notesMarkdown`, `__lh.scoreFacts`.
- Mac: `Cv.snapshot(app, w, h, path)` renders into gfx buffer 11, copies pixels into a JS_LICE bitmap, writes JPEG (needs js_ReaScriptAPI); `score_image_uri()` base64s it. "Copy notes" leaves the picture out (clipboard); "Export notes…" includes it. Check script: scratchpad v23.lua.

- Mac v2.3.1: export adds "REAPER only link: [Open the project … in REAPER](file://…rpp)" under the title (percent-encoded path from EnumProjects(-1)); says none if the project is unsaved.

## iPad v53 / Mac v2.4 (6 Nov 2026): regions and markers lanes; tool hints removed
- Sketch JSON: `markers [{id, t, name}]`, `regions [{id, a, b, name}]` (seconds from score start). In undo, Insert silence (shift / extend a region crossing t) and Remove time (markers inside deleted; regions clipped, dropped if < 0.01 s).
- Two lanes above the plot (regions 2–15 px, markers 16–29 px; plot top 34 iPad / LANES_H 32 Mac). Markers: plum triangle + faint dashed line through the score; regions: muted tinted bars (4-colour cycle) with faint edge lines.
- Click/tap markers lane = add; drag regions lane = new region; drag = move; region ends = resize; double-click/tap = name (iPad #mrBox, Mac GetUserInputs separator |); ⌥-click or ⌫ = delete; ⇧M marker at pointer; ⇧R region from time selection (+ tsel bar / context menu / Score tab button).
- Obsidian export: "Regions and markers" section + count in key data; lanes appear in the score picture.
- Mac Commit: `write_markers` writes them as REAPER markers/regions at anchor + t; previous ones (sk.mac.mr_written) deleted first. Not yet run against a real project.
- iPad hud no longer shows tool hints (hint()/annHint() unused for it); hud sits under the lanes and hides when empty. Mac: removed the "Editing notes: …" banner at the top of the chord-edit column.

## iPad v53.1 / Mac v2.4.1 (6 Nov 2026): Tap markers; iPad opens blank
- Tap markers (⇧T, Score tab button): PulseSketcher-style P / Q streams. Markers get `kind: "P"|"Q"`, green / orange, labels P1, Q1… (count in time order). Taps land at the playhead while the score plays, else on a clock from the play point (auto P at the start). Return = done, Esc = cancel (undo). iPad bar #tapMkBar with P / Q pads; Mac Score tab pads + status line.
- Mac Commit names unnamed tapped markers P_001 / Q_001 with PulseSketcher colours.
- iPad start-up: always a blank score (example sketch removed); if the browser autosave holds work, an ask bar offers "Reopen" (a spare copy kept in STORE_KEY + '-previous').

- Mac v2.4.2: fixed "attempt to call a nil value (arc_drag_ctrl)" while drawing an Arc (local used in draw_op before its definition; now forward-declared). Scanned all lhs_*.lua for the same pattern: none left.

## iPad v53.2 / Mac v2.4.3: Tap markers = time points
- One stream only (key P / Tap pad), kind "TP", green. First tap = TP0 at the play point (or the playhead while playing); later taps TP1, TP2… at their offset from the first. No auto marker on start. Labels in time order (stable sort); REAPER names TP0, TP1…; Obsidian lines "- **TP0** 00:04:00". Old P/Q markers still display.

- iPad v53.3: the marker/region name box no longer pre-selects its text (selected text made iPadOS show its text menu with "Send to Claude"); caret goes to the end.

## Mac v2.4.4: sketches save to iCloud by default
- default_dir() = iCloud Drive › "00 – LH Spectral Sketches" (created if missing; LH_PORTABLE All Sketches only if no iCloud). Save as / Export notes start there unless the current file is already in iCloud. ⌘S on a file outside iCloud asks: Yes = Save as into iCloud, No = overwrite in place, Cancel.

## Mac v2.4.5 (6 Nov 2026): pulse glitches + microtonal moves
- Diagnosis (Sketch 02, eighth-tone field, 6 overlapping pulses on Breath): stretch/compress had pushed rates to 77 / 25 / 12 Hz; allocate() ran out of channels idle ≥ 1 s and reused channels 6 ms after note-off, so the next pitch's bend/retrigger cut release tails ("voice robbing", glitchy).
- Fix 1: pulse voices carry `group` ("_pulse"..partial); Commit gives each pulse train (per unit, per partial) its own channel for its whole span; pulses re-attack the same voice. Sketch 02: 250 notes → 6 channels, 1 bank, 0 overlaps. `Commit._allocate` exposed for tests (scratchpad v245.lua).
- Fix 2: Model.PULSE_MAX_HZ = 40 (25 ms gap) in pulse_times, stretch, inspector and brush sliders (min gap 25 ms, was 5).
- Fix 3: moving units snaps the primary unit's reference pitch (Cv.ref_pitch) to the field when snap is on (within 1.2 st), else semitones; chord blocks keep semitones; ⌃ = free. Creation and pulse end-handles already used the field.
- iPad parity still to do: same 40 Hz cap; iPad move has no pitch snap at all (free) — decide whether to add field snap there.

## Synth voice fix (6 Nov 2026) — the real cause of the 0:24 glitch
- LH_FM_Texture_Synth_v2 has 8 voices total; with Release 3000 ms every note held a voice ~27 s, so new notes always stole voice 0 (hard cut + random phase = click). Sketch 02: 235 of 250 notes stole a playing voice.
- Fixed in LH_FM_Texture_Synth_v2, LH_FM_Texture_Synth_CC_v2, LH_Additive_Texture_Synth, LH_Subtractive_Texture_Synth (backups: LH Score Tool/backups/synths_before_voicefix_2026-11-06): note-on 1) re-attacks a voice with the same note + channel (keeps phases; pulse trains), 2) else a silent voice, 3) else steals the quietest releasing voice. Simulated on Sketch 02's MIDI: 0 steals. Breath / Sandstorm / Modal not checked (no "found = 0" pattern).
- Attack advice: 2–5 ms, not 0 (0 = 1-sample attack → click on every note).

## Mac v2.4.6 (2026-11-06) pulse onset/offset
Pulse params onset_ms (def 3) / offset_ms (def 10): per-pulse CC11 fade in/out in pulse_voices gain, so pulses are clean whatever the synth ADSR. Inspector sliders Onset 0-100 ms, Offset 0-500 ms. iPad parity TODO. Synth Attack defaults now 3 ms (Breath left at 4 s).

## Mac v2.4.7 (2026-11-06) pulse shape + voice fix 2
Pulse param shape (superseded in v2.4.8); onset/offset now raised-cosine. iPad parity TODO (shape, onset_ms, offset_ms).
Voice choice now also in Breath, Sandstorm Combs/FM, Wind Organ, Modal, SpatialNoise v2.6, SpatialSub v1.5: same note+ch re-attacks own voice, else free, else quietest/oldest releasing, else quietest/oldest; reused voices keep state (no click). Backups: backups/synths_before_voicefix2_2026-11-06. Not yet compiled in REAPER.

## Mac v2.4.8 (2026-11-06) pulse grain morph
Pulse params pshape (0 Flat, 1 Grain, 2 Triangle) + grain 0..1 (0 strike: instant peak falling ~48 dB; 0.5 bell; 1 swell: rising into the cut; between = peak moves, curves blend). Model.pulse_shape_of reads v2.4.7 `shape` when pshape is missing. iPad parity TODO.

## Mac v2.4.9 (2026-11-06) microtonal grid
A microtonal field (any pitch >5 c off 12-TET) is the pitch grid for moves, handles and drawing even with Snap off (grid_on = snap or field_micro). Non-micro field: Snap on = field, off = semitones (moves) / free (handles). Ctrl = free. Also: all LH synth Attack defaults 3 ms incl. Breath and Spatial Sub (amp+filter). Pulse drawing: tick at peak + faint bar (draw_voice pulse branch). iPad parity TODO.

## Mac v2.4.10 (2026-11-06) commit at cursor
Commit: if the edit cursor (or play position while playing) differs from sk.mac.anchor_s and was not placed by the tool (app.set_cursor / app._tool_cursor), Yes/No/Cancel: Yes moves the anchor there. Manual section 5 updated.

## Mac v2.4.11 (2026-11-06) commit = cursor, no markers in REAPER
Commit: anchor = edit cursor every time (unless the cursor is where the tool left it, app._tool_cursor). No dialog. Commit.run no longer calls write_markers or ensure_region (kept in lhs_commit for a later option). Score tab "Start at the edit cursor" button removed. Manual section 5 rewritten.

## Mac v2.4.12 (2026-11-06) numbered layers
Layers are named Layer 1, Layer 2… (new sketches, + Layer menu, and normalize renames a layer whose name still equals its preset name). Layer ids unchanged (breath, fm…) for iPad compatibility; + Layer menu items read "Sound: Breath (LH_Breath)". iPad parity TODO: same naming.

## Mac v2.4.13 (2026-11-06) field axis
Left axis follows the field: chromatic = note names as before; any other field = its own pitches as axis labels (pitch_label, priority C > whole notes > quarter tones > rest when crowded), field lines always drawn (not only with Snap), partial numbers in-plot for harmonic-type fields. iPad parity TODO.

## Mac v2.4.14 (2026-11-06) margin labels
GUT_L 46 -> 66. Harmonic-type fields: partial number follows the note name in the left margin ("E4-14  5"), nothing drawn over the score; low partials win when crowded.

## Mac v2.4.15 (2026-11-06) layer-at-a-time workflow
Commit button = "Commit layer": writes only the active layer (Commit.run opts.layers); ⌥-click "Commit all". ⌘Return = active layer. Audition: one shared hidden folder per project (AUD_KEY "shared"; an old per-sketch folder is adopted), children keyed slot|n|bank (no engine in key), synth swapped in place, so listening never adds tracks. L._aud_slot is runtime-only (json skips _ keys). iPad n/a.

## Mac v2.4.16 (2026-11-06) layer list order
Layers panel lists Layer 1 at the top down to Layer 7 (sk.layers order); Move up/down follow the list. iPad parity TODO.

## Mac v2.4.17 (2026-11-06)
S (plain) = Select tool, as well as V (S alone was unused; ⌘S save, ⇧S unchanged).

## iPad v54 (2026-11-06) — catches up with Mac v2.4.5–2.4.17
- Pulses: at most 40 per second (the gap slider starts at 25 ms). New Shape (Flat / Grain / Triangle), Grain (strike – bell – swell), Onset 3 ms and Offset 10 ms, the same as on the Mac. Old Mac `shape` files are read too. The shape is applied to the sound and to the drawing: each pulse shows a tick at its peak.
- Moves snap like on the Mac. With Snap on, or in any microtonal field, a moved unit lands on the field; otherwise it lands on semitones. ⌘ / ctrl moves freely, and chord blocks keep semitones. Drawing and handles use the same rule.
- Axis: the left margin is 66 px. Partial-type fields show pitch + partial number. When labels crowd, C comes first, then whole notes, then quarter tones; low partials win.
- Sound Lab: the default attacks for Breath, Additive, FM and Resonant bands are 3 ms.
- Already at parity: layers are named "Layer n", 1 is at the top, and S switches Select / draw.
- Backup: ipad/lh-spectral-palette-sketchpad_v53.3_backup_before_v54.html

## iPad v55 (2026-11-07): saving and layer sounds
- **Naming:** a new sketch asks for its name once, at the first Save. The name is filled in as "Sketch YYYY-MM-DD HH-MM" and can be edited. After that, Save uses the name without asking. "Untitled sketch" counts as unnamed. Saves can't run twice at once.
- **Layer sounds were forgotten:** the Sound mode wasn't restored and defaulted to plain sine. It now defaults to "Sine + Sound Lab presets", is remembered, and is restored from the sketch. Any sketch whose layers have sounds plays them.
- **Unsaved check:** changes to layer sounds, layers and Sound mode now count as unsaved changes.
- **Sound Lab:** edits are kept automatically when you close the Lab, switch presets, or use the sound on a layer. Editing a built-in sound makes your own copy, and the layers using it move to that copy. Revert still goes back.
- **iCloud:** the iPad can't overwrite iCloud files silently from a web page, so the Files sheet still appears on every save. Choose Replace there to keep one file.

## iPad v56 (2026-11-07): zoom and 0:00, segment curves, drop-downs
- **Zoom:** units, selection outlines and handles are clipped to the score area. When zoomed in, nothing draws left of the visible start or past 0:00.
- **Moves stop at 0:00:** dragging, or nudging with the arrow keys, stops when the earliest unit of the selection reaches 0:00. A sketch that opens with units before 0:00 has them moved to 0:00.
- **Segment curves:** in the envelope lane, a small curve button sits under the middle of each segment, as in Craft. Tap it to choose that segment's curve: Linear, Exponential, Logarithmic, S-curve, Smooth or Hold.
- **Drop-downs:** a drop-down lets go once you pick from it, so Space no longer reopens it.

## 7 Nov 2026: LH synth rename + iPad v57
- **REAPER synths** (Effects/01_LH_SynthToolkit):
  - LH_Synth_ Additive, Breath, FM, FM_Chord, Modal, Organ, Subtractive.
  - LH_Proc_ Accord, AM_Pitch_Modulator (title "LH_Proc_AM + Pitch Modulator"), Gentle_Panner, Spat_Panner.
  - Sandstorm Combs, Sandstorm FM and Wind Organ are unchanged.
- **One FM synth:** LH_Synth_FM merges FM v2 and CC v2. Live Controls (slider 13) is off by default. It has 21 merged presets.
- **Organ and FM Chord:** both are no-wind copies. They keep the same controls and presets as their parents, with the wind, gust and sand controls hidden and held off.
- **Archive:** the old files and the Spatial Sub / Noise Synth / Noise Osc synths are in 01_LH_SynthToolkit_Archive.
- **Dance Piece:** its 181 projects are untouched. Copies of the six old synths they use stay under their old file names, with titles beginning "zz Dance Piece -". FM v1 and CC v1 were already missing before today; those copies fix that.
- **Other projects:** 21 were updated to the new names. Their backups and the earlier list are in LH Score Tool/backups/rename_2026-11-07 and LH Score Tool/Projects_to_update_2026-11-07.txt.
- **Presets** moved with their synths; the old preset files are in presets/_pre_rename_2026-11-07.
- **Add FX folders:** "LH Synths" and "LH Processing". reaper-jsfx.ini was updated by hand.
- **Scripts:** the Score Tool, Harmonic Extenders and Accord UI use the new names. Old engine ids still work through Model.ENGINE_ALIAS on the Mac and ENGINE_ALIAS on the iPad.
- **iPad v57:**
  - new engine names;
  - the Sound Lab shows a note that the iPad plays an approximation;
  - "Use in the score" is at the top of the left panel;
  - the Sound Lab has synths only, never LH_Proc_ effects.
- **Tested** in REAPER: all synths load with their controls and presets (loaded the way a project loads them), and the libraries load.
- **Later on 7 Nov:**
  - The six Dance Piece effects are restored byte-for-byte, with their original titles. No Dance Piece project was changed.
  - 01_LH_SynthToolkit_Archive moved out of Effects to `Reaper Application Support/Effects – Archive (not scanned)`, so it no longer appears in the FX list. Three old sketch projects that pointed at the archived Spatial synths will show them as missing.
  - The test entry is gone from reaper-jsfx.ini.
  - Add FX folder order is now LH Synths, LH Processing, Favorites, Spatial Modulation Tools.


## Standalone (offline) iPad app, 7 Nov 2026

- **Why:** the claude.ai link needs sign-in and internet on every open (it went straight to the claude.ai sign-in page when tested), so it can't run on a plane.
- **Build:** `standalone/build.py` turns the newest `ipad/…_vNN.html` into `standalone/site/`. That folder holds index.html, manifest, the offline-cache script sw.js, and icons. The artifact file itself is not changed.
- **Saving:** claude.ai's save feature is replaced by the iPad Share sheet (Save to Files), with a plain download as fallback. Cancelling shows "Save cancelled".
- **Offline:** everything is cached on first open; Google fonts are cached the first time they load. A new build replaces the old cache, and updates arrive in the background when online and show on the next open.
- **Tests:** saving was tested in the browser pane, where Share, Cancel and the download fallback all work. The pane blocks offline caching altogether (even an empty test script), so the cache was tested in a Node simulation: installs, opens offline, caches fonts, leaves other sites alone. *Not yet tried on the real iPad.*
- **Hosting:** GitHub Pages at https://l-sial.github.io/spectral-score/ (public repository L-SIAL/spectral-score).
  - The local repository is `standalone/site/.git`. Author: L-SIAL with a noreply email.
  - Sign-in goes through the gh tool in Code Development/tools (sign-in key in the laptop Keychain), linked by `.git/gh-cred.sh`. Nothing in the global git config.
  - **To update:** `python3 standalone/publish.py "what changed"` rebuilds the app and pushes it.
- **Moving over:** the installed app has its own storage, separate from the claude.ai link.
  - In the old link, save the open sketch, then Library… › Export library… (units and Sound Lab presets).
  - In the new app, Library… › Import library….
- **Every new iPad version:** run `python3 build.py`, then upload `site/`.


## iPad v58: sketches kept in the app, 7 Nov 2026 (artifact version 76, plus the offline app)

- **Save** keeps the sketch inside the app (IndexedDB `lh-spectral-sketches`, with a localStorage fallback). The first save asks for a name; later saves are one tap. If a name is already taken, the app adds " 2".
- **Open…** opens a "Sketches on this iPad" list. Each entry shows when it was saved and whether it has been sent to iCloud (it is "sent" only if that exact save went out, so a wrong clock on the Mac can't hide an unsent edit). Rows have Open, Send… and Remove; the list also has "Open a file from iCloud…" and "Send all unsent" (several files in one share sheet, offline app only).
- **Send to iCloud…** (Sketch section) saves first if needed, then opens the share sheet. On the claude.ai link this uses its own save feature.
- **Sketch id:** the iPad uses the Mac's `id` field, and the iPad writes `saved_on: "iPad"`. The Mac's `Model.prepare_for_save` now writes `saved_on = "Mac"` (lhs_model.lua; backup in the session scratchpad).
- **Opening a file** matches it to a stored sketch by id, then by name. If the iPad copy is newer, the app asks which to open (Keep the iPad copy / Open the file). Choosing the file keeps the newer iPad copy as "Name (iPad date time)". Opened files are stored in the app and count as sent.
- **Tested** in the browser pane: save, renaming, the list, Send, Send all, the older/newer check, a Mac clock running ahead, and Remove. No errors.

## iPad v59–v60 + Score Tool: one shared library (7 Nov 2026)
- **v59:** the open sketch's name is always in the bottom strip (tap = the iPad sketch list); a Mac sketch named "Untitled sketch" takes its file name. Version label (v59/v60…) at the bottom right shows which build is running.
- **v60 shared library** = units (saved units/groups) + Sound Lab presets, the same on both machines.
  - Every item has `modified` (ISO UTC). Merge: by id, the newer `modified` wins; `deleted` / `library_deleted` = {id: when}, a deletion wins over anything older. Legacy items without a stamp count as oldest.
  - Edits are stamped automatically: each side remembers the content it last saw (canonical JSON without modified/builtin) and stamps `modified` when it changes.
  - **Inside every sketch:** `unit_library`, `sound_library` (all presets, with `mac`), `library_deleted`. Opening a sketch on either side merges it ("Library: n new, n updated, n removed" in the status).
  - **Mac:** master copy in iCloud Drive › … LH Spectral Sketches › `LH Library.json` (+ copy in REAPER/Data/LH Score Tool). Every library save re-reads the iCloud file and merges first, then writes both. Opening the Unit library (Y) re-reads iCloud. Delete leaves a tombstone. Layer menu › Sound lists every library sound (copied into the sketch's ipad_sounds.presets when chosen, and refreshed to the newest version on open/save).
  - **iPad:** Library… › Import/Export still work (same merge, "already up to date" when nothing changed); usually not needed because sketches carry the library.
  - Lua code: lhs_edit.lua (shared library section), lhs_app.lua (write_file, set_sketch, lib_import/export, draw_library, layer menu). Tested in REAPER against a sandbox copy (9 checks). Backups: scratchpad v60/mac_bak (session only).

## Mac Sound Lab (Score Tool, lhs_lab.lua) + iPad v61 (7 Nov 2026)
- **Open:** header ♪ Sound Lab, or key 3. Done / Esc / 3 closes (asks to save changes).
- **Controls come from the JSFX file:** slider lines are parsed (default, range, step, :log, {options}); "-" hidden sliders are kept in presets but not shown; "Group: name" labels become section headings. Pitch Bend Range and Output Mode are left to Commit; a chord synth's "Source" is held on MIDI notes while the Lab plays.
- **Live sound:** a hidden temporary track "LH Sound Lab (temporary)" (P_EXT:LHScore_soundlab), input = virtual MIDI keyboard (I_RECINPUT 6080), armed, monitoring on, record mode none. Notes via StuffMIDIMessage(0, …). Pads (mouse hold), keys A W S E D F T G Y H U J K (hold; Z / X octave), Space test phrase, Notes off. The track is deleted when the Lab closes or the window closes. Other armed tracks listening to the virtual keyboard would also sound.
- **Log sliders:** TrackFX_SetParam takes ln(value) and GetParam returns ln (checked in the portable REAPER: 0.3 in → 0.3 shown).
- **Presets:** left column = shared library sounds for this synth, then the plug-in's own REAPER presets (read by stepping through them on the Lab track) and Plug-in defaults. Save → shared library {id "um…", name, engine (iPad id), made_on = "Mac", params {}, mac = {engine, sliders}}; iPad-made presets and REAPER presets are never overwritten (Save makes a Mac copy). Sketch copies of a saved preset follow it. "Use on <layer>" saves if needed and assigns it to the active layer.
- **iPad v61:** Mac-made presets keep their full mac.sliders (soundForFile no longer regenerates them), params are derived from the sliders for the iPad's approximation (paramsFromMac), shown under "From the Mac"; saving one on the iPad makes an iPad copy.
- **Tested** in the portable REAPER (scratchpad v60/labtest.lua, run in a new project tab): all 7 synths load, controls parsed (Breath 17 shown, Organ 29 + 19 hidden, FM Chord 20 + 35 hidden), REAPER preset counts read, set/get round trip incl. log sliders, Lab track created and removed. Not yet tested by hand: the drawing/interaction and live sound.
- **Testing note:** the portable binary is …/23 – Reaper_Portable/Reaper Application Support/REAPER.app — NOT /Applications/REAPER.app (that is the laptop install).

## iPad v62: Subtractive, Organ, FM Chord (7 Nov 2026)
- New engines LH_Subtractive, LH_Organ, LH_FM_Chord (ENGINE_DEFS / ENGINE_MAC / ENGINE_ORDER / SHORT), ported from the JSFX:
  - Subtractive: saw / band-limited pulse (PeriodicWave per duty) / triangle / pink noise, unison 1–4 with detune, white-noise mix, biquad LP/BP/HP with the SVF's Q = 1/(2(1−res)) (BP keeps peak gain Q), key tracking via fp, drive (x/(1+d|x|), 2× oversampled), one-pole attack/release, the plug-in's pan (by pitch for one voice, centre for unison).
  - Organ / FM Chord share pipeSource(): carrier + feedback modulator (fmModWave), 1:3.5 halo, Organ stops (16′ 4′ 2⅔′ 2′ 1⅗′, rk_norm), celeste and stereo detune on the right, tremulant (level + ±12·depth cents), ±33 % index wobble, Organ chiff grains at note-on, one-pole output low-pass (IIRFilter), linear attack + decay/release with time constant ms/4.
  - Levels follow the plug-ins (K_FM·√2·√½·K_OUT·gain × ENG_K): Organ / FM Chord sound ~15 dB under FM/Additive, as in REAPER.
- Controls and all REAPER presets (16 Subtractive, 16 Organ, 26 FM Chord) generated from the plug-in files and the presets/*.ini banks by scratchpad v62/gen.py (Data = hex of space-separated slider values + name).
- Mac lhs_commit.lua: setup_synth_fx now also sets "Chord: Source" = MIDI notes (Organ / FM Chord), otherwise those synths played their drone and ignored the score.

## v63 modulation envelopes, iPad + Mac (7 Nov 2026)
Up to 3 per unit, each moving one control of the layer's synth across the unit (values replace the preset's).
- **Data** (both sides): `unit.mods = [{k, s (plug-in slider), e (iPad engine id), l (label), pts}]`; pts are `[pos 0–1, value 0–1 across the control's range (log controls on a log scale), curve, tension]`. Split slices them.
- **Controls** (curated, per voice): Breath bandwidth/floor/note width/output gain · Additive harmonic decay/master amp · FM index/sub mix/master amp · Modal output gain · Subtractive cutoff/resonance/noise mix/master amp · Organ index/halo/5 stops/low-pass/output gain · FM Chord index/halo/low-pass/output gain. Lists: iPad `MOD_KEYS`, Mac `Env.MOD_DEFS` (lhs_env.lua) — keep them the same.
- **iPad v63**: "Modulation" row under the Loudness/Pan row: chips, "+ Add envelope", control drop-down, Remove. Lane grid in the control's units, point read-out. Playback: `unitVoices` builds per-voice curves (`x.mods`), engines expose `mods(mv, n, t0, dur, el)`; index wobble / shimmer / drift ride on top. Organ/FM Chord modulated low-pass is a biquad on the iPad (one-pole can't move in Web Audio). Test hooks `__lh.modTest`, `__lh.unitVoices`.
- **Mac MIDI** (14-bit, per channel, `LH_ModLanes.jsfx-inc` in 01_LH_SynthToolkit): slot k target CC 102+k (slider number, 0 = off; sent with every note), value CC 16+k/48+k every 10 ms while moving (sooner on a 64-step jump), each value 10 ms ahead because the synth glides over the gap. Commit only sends lanes made for the layer's synth.
- **Synths**: all 7 LH_Synth_* import the include (backups in `LH_Synth backups/2026-11-07 before mod lanes`). Organ/FM Chord: a lane on low-pass gives that note its own one-pole outside the shared one.
- **Score Tool**: envelope header "Lane: … ▾" — Loudness, the lanes, Add envelope ▸, Change control ▸, Remove. LFO, Record and the level row are loudness-only.
- **Not yet tested in REAPER** (Lua syntax, JSFX compile, render) at the time of writing.


## v64 (7 Nov 2026): more modulation controls, Flat fix, update prompt, Mac tested; Manual + Tutorial

- **Mac v63 tested in portable REAPER.** All 12 Score Tool lib files load. All 7 LH_Synth_* compile. A commit writes the target CCs (102–104) and 14-bit value pairs (16–18 / 48–50). Renders show each lane moving its control: +7 to +17 dB level rises, Subtractive centroid 400 → 900 Hz, and notes without a lane stay at the preset.
- **v64 controls** (continuous only), iPad + Mac, in MOD_KEYS (iPad) and Env.MOD_DEFS (lhs_env.lua):
  - Breath: tune s16, pitch drift s10.
  - Additive: fund ratio s2, inharm s4, detune spread s8, shimmer s9.
  - FM: carrier ratio s1 (log), mod ratio s2 (log), feedback s4, index drift s8, ratio drift s9.
  - Modal: inharm s7, mode detune s9.
  - Subtractive: unison detune s14.
  - Organ: mod ratio s24, stereo detune s27, feedback s28, celeste s37.
  - FM Chord: mod ratio s39, stereo detune s21, feedback s22.
- **JSFX.** Per-voice substitutions; the backups are in LH_Synth backups/2026-11-07 before v64 controls.
  - Breath's drift is now a unit wander scaled by the depth.
  - Modal keeps m_base / m_jit per mode, and remode_voice() re-tunes every 16 samples while a lane drives s7 / s9.
  - Organ / FM Chord have per-voice c_mrl, c_mrr, c_cel, c_fb.
- **iPad engines.**
  - Ratio, tuning and detune changes go onto oscillator/filter `detune` in cents, so they combine with pitch glides.
  - FM index compensation keeps the plug-in's PM index (deviation in Hz scales with the ratios).
  - A feedback lane crossfades 5 phase-locked modulators (fbW).
  - Modal uses modalRat().
- **Tests.** iPad: 22 controls each change the render, no NaNs. Mac: renders confirm Breath tune (215 → 227 Hz), Additive ratio, FM mod ratio (centroid 400 → 3700), Organ mod ratio, FM Chord feedback, Modal inharm. The Lane ▾ menu itself is not hand-tested.
- **Flat.** On a Pan lane it means centre; on a modulation lane, the preset value (iPad and Mac). Saved-shape LFOs apply on Loudness only (Mac).
- **Offline app.** It shows an "A new version has downloaded" bar with Reload now / Later (on controllerchange; build.py TAIL), and calls reg.update() on load.
- **Published.** Offline app "v64-20261107-1930"; artifact version 82.
- **Docs.** In `LH_Palette_Handoff/Manual/`: Manual, Tutorial (24 studies), Space and Separation (panning ideas), Before You Travel (test routine).
- **Not done.**
  - The old effects-list clean-up: the six Dance Piece synths still show under their old names. That needs the user's decision, because they're the user's files.
  - A stray empty folder `/Volumes/LH_PORTABLE/01 – Projects` (plain space) was created by mistake on 7 Nov. It is not deleted; waiting for the user's OK.


## v65 (8 Nov 2026): Spatialisation — spectral spatialisation, one place and path per voice

**The idea (keep it in every future manual):** the score is MIDI with one channel per voice *so that* each component of a complex or micro event (a partial, a grain, a pulse) can have its own position and movement. Space is composed inside the sound.

- **Data (sketch file, both devices):** `space = {law, spread 0-1, rotate turns, pattern, step, seed}`, `spread_env` beside `pan_env` (same point format, 0-1).
- **Shared maths** (iPad `spaceHome` / `applySpace`; Mac `Model.space_home` / `space_fns` in lhs_model.lua): hash(seed,i) = Park-Miller ×3 on (seed % M31 + i·7919 + 1); pitch rank k by round(ftom·100), onset index j by round(t0·1000), entry rank by (t0, f0). Laws centre/pitch/pitch_rev/fan/oddeven/zones/golden/entry/random; patterns fixed/pingpong/sweep/walk/random/cycle; home = law, or pattern, or clamp(0.7·pattern + 0.3·law). θ = (pan_env·2−1)·90 + spread·h·90 + 360·rotate·u. Stereo = 0.5 + 0.5 sin θ. **Verified identical** JS vs Lua on 54 law × pattern cases.
- **MIDI:** CC105 1/0 per voice at note start; CC10/42 14-bit azimuth (0-1 turn, 0 front, 0.25 right) every 10 ms while moving, 10 ms ahead (as the mods). Moving event patterns drop pulse channel-sharing (each pulse own channel).
- **JSFX:** `LH_ModLanes.jsfx-inc` gains lhs_* arrays (base+432..575), glide the shortest way round, `lhs_pan(ch)` / `lhs_az(ch)`. All 7 LH_Synth_* use it (Breath's own CC10/42 handler removed; Modal spreads modes around it; Organ / FM Chord in MIDI mode). Backups: `LH_Synth backups/2026-11-08 before spatialisation/`.
- **Mac UI:** Lane ▾ › Pan (centre) / Spread (pseudo mod lanes, `st.target` "pan"/"spread", SPACE_DEFS in lhs_env.lua); inspector Unit tab › Spatialisation; split slices spread_env.
- **iPad UI:** lane switch Loudness | Pan | Spread; Settings › Unit › Spatialisation (Law, Spread, Rotation, Events, Walk step, New space seed).
- **Tested:** REAPER portable render, all 7 synths: pan lane hard L / R lands (Modal ±24 dB, its modes keep their spread), pitch law + rotation moves, Breath ping-pong pulses alternate. iPad v65 in the browser: positions, UI, playback, no errors. Mac Lane ▾ / inspector not yet tried by hand (Before You Travel B10).
- **Published:** offline app v65-20261108-0844-e9eb58; artifact version 83.
- **Next:** multichannel (Spat Panner reading the same azimuths, 4/8 ch), then the OM# spat port; harmonic/inharmonic law, counter-rotation, accent / rate-linked pulses, decorrelation law.

## v66 (8 Nov 2026): stacked lanes; "Spatialisation" drop-down

- The Law drop-down is labelled **Spatialisation** on both devices.
- **Stacked lanes, both devices:** a Stack toggle shows the unit's other lanes (order Loudness, Pan, Spread, mod 1-3; the one being edited excluded) as compact read-only rows above the editor, same time axis; tap/click a row to edit it; up to 3 visible, scroll for more. Shown = explicit choice per group (vol/pan/spread/mod) or, by default, the drawn ones. Tall rows option. iPad: `renderStack` / `drawStrips`, localStorage `lhLaneStack`, the stack takes its height from the editor (min 120 px). Mac: `stk` + `stack_list` in lhs_env.lua, ExtState `lane_stack`, Stack button beside Lane ▾, Lane ▾ › Show in stack / Tall rows.
- Tested: iPad in the browser (rows, switching, scrolling, no errors); Mac Lua loads in REAPER; **Mac stack not yet tried by hand** (Before You Travel B11).
- Published: offline app v66-20261108-0909-403eb8; artifact version 85. lhs_app.lua / lhs_env.lua also copied to the LH_PORTABLE_mini REAPER install.


## v67 (8 Nov 2026): Save as new
- Score › Sketch: **Save as new…** button under Open… / New, and ⇧⌘S. Asks a name ("<name> copy"), saves a copy with a new sketch id, opens the copy; the original keeps its last saved state.
- askName(asNew) swaps the sheet title/note. Mac parity: check the Score Tool has an equivalent Save As (Mac side to do).

## v68 (8 Nov 2026)
- Save as new… and Send to iCloud… on one row (.selrow.pair). The Score panel no longer overflows: the Field selects shrink (section grid minmax(0,1fr)).
- v69: version number moved to the bottom-left corner (.statusrow .ver order -1).

## Next round (queued 8 Nov 2026)
Queue started 8 Nov 2026, after v69. Copy into LH_Palette_Handoff/HANDOFF.md ("Next round") when LH_PORTABLE is mounted. It was unmounted when this was written.

0. **Audio stuck silent (priority, 8 Nov).** On the iPad, playback first glitched, then went silent (the play head still moved) after an output change or interruption. It only came back after the app was fully closed twice.
   - Cause: ensureAudio() resumes only when ac.state === 'suspended'. iOS uses 'interrupted'.
   - Fix: resume when state !== 'running'; if that fails, rebuild the AudioContext and master chain; also resume on visibilitychange, pageshow and statechange.
   - The original glitch is still unexplained. Tests to run: 1 (hide the envelope panel → v66 stack drawing?) and Sound = Sine (synth load / v65 per-voice panners?).
1. **⏮ Return to 0:00** (agreed). A button beside Play, plus Return/Home, set the play start to 0:00 AND scroll the view to the start. Today Return/Home only call setPlayFrom(0); the view doesn't move and there's no button. Mac Score Tool: do the same.
2. **Focus for drawing** (undecided). Mockup options:
   - A: a Focus toggle that hides the panels and lanes and restores them;
   - B: the envelope panel folds to a thin bar, with Shapes/Curve/Modulation/Stack under "More";
   - C: lanes open only when a unit is selected.
   I recommended A+B. Keys 1/2/F already hide the panels separately.
3. **Mac parity for v67 Save as new**: the Score Tool needs a matching Save As (check whether it exists).

4. **[ ] zoom centres on the play head** (user request). Today zoomAnchor() goes hover/pointer → selected unit → cursorT, then clampView, so the head drifts off-centre. New rule for [ ] and the zoom buttons: centre on the play head (the moving head while playing, else the play start / cursor). Pinch keeps its finger anchor. Mac: the same.


## v70 (8 Nov 2026): one-row envelope panel
- Lane ▾ (Loudness/Pan/Spread + modulation lanes, + Add, control, Remove), Shape ▾, Curve ▾ (types, New points, Tension, Apply to all), Stack ▾ (Show the stack, lanes, Tall rows), Edit ▾ (Copy, Paste, Reduce, Delete point, Reset, LFO, Section). Loop / Record stay as buttons.
- Built by moving the existing controls into .lpop popovers at startup (IIFE at the end of the script), so all wiring is unchanged. Picks close Lane/Shape/Edit (capture-phase listeners, because modChips/shapes re-render). Outside tap or Esc closes.
- Saves about 4 rows (~140 pt) for the score. Mac: Lane ▾ exists; check the Score Tool envelope panel for the same compaction (parity).
- Manual §7 needs the new menu names.

## v71 (8 Nov 2026): which lanes a unit has
- Lane ▾ lists the unit's lanes: ● drawn / ○ flat, tap to edit, Shown/Hidden = in the stack (per lane now; stackKey is the identity; the Stack menu's Show chips are hidden). Showing a lane turns the stack on.
- Loudness counts as drawn only when it is not flat (volDrawn) or has an LFO.
- Lane marks on units in the score: L P S 1 2 3 (plum; teal = the lane being edited). Tap one with the Select tool or a finger (or ⌘): select the unit, open the panel, edit that lane. Score › "Show lane marks on units" (localStorage lhEnvMarks).
- Bridge: window.__lhMarks / window.__lhLane (the v70 menu IIFE sits outside the main block).
- Mac parity: ● in Lane ▾ exists; add per-lane stack eyes and the unit marks.

## v72 (9 Nov 2026): playback engine
- **Concurrency budget:** selectVoices() keeps the loudest voices within a budget for what sounds AT ONCE (it used to cap the whole score, so long scores lost later units). Score › Playback detail: Light 170/70, Normal 300/120 (default), Rich 480/200 (cost units / voices); localStorage lhPlayDetail.
- **Honest costs:** voiceCost(); FM Chord and Organ use pipeCost(). It was 4; the real cost is about 11 for a full stereo voice.
- **Lighter quiet voices:** among overlapping voices, the 14 loudest keep the stereo-detuned right side (PIPE_RICH) and 28 keep the halo (PIPE_HALO, only above −40 dB); the others are built mono. Rank = _i (the number of louder voices it overlaps).
- **Look-ahead feed:** voices are scheduled 4 s ahead every 0.7 s, so Play starts at once.
- **Measured** (offline render, Mac Chrome, 70 overlapping FM Chord voices): old 0.237 × real time; Rich 0.125 (all 70 kept); Normal 0.098 (47 kept); Light 0.052 (16 kept). 14 voices (3 default bands): 0.047. Sine: 0.004.
- **Play head delay:** pos −= soundDelay(). Auto = ac.outputLatency || baseLatency, or a manual 0–400 ms (Score › Play head delay; lhPhDelay). For AirPods.
- **Stuck audio:** ensureAudio resumes from any non-running state; onstatechange / visibilitychange / pageshow / focus wake it. If the clock doesn't move for 1.2 s after Play: stopPlay + rebuildAudio() (clears fbWaves / pulseWaves) + "Press Play again".
- Test hooks: __lh.selectVoices / voiceCost / renderTest / setSound / setDetail.
- Mac: not affected (the real synths do the work).

## v73 (9 Nov 2026)
- PLAY_DETAIL now also sets how many voices keep the stereo side / halo: Light 6/12 (budget 200/80), Normal 28/56 (420/160), Rich all (1200/260) = the pre-v72 build. Measured (70 overlapping FM Chord voices): Light 0.065, Normal 0.13, Rich 0.229. Three default bands (14 voices) are built in full on every setting.

## v74 (9 Nov 2026)
- Playback continues past the score end until the last voice's release ends (≤ +10 s); the play head waits at the end. Open: the user's 3-band FM Chord score lost its tails (the bands end at 0:20 in a 1:00 score, with loudness ending at max); a fresh band has a tail. Awaiting the file.

## v75 (9 Nov)
- Fixed missing release tails on some bands: bandVoices used ceil for the step count, leaving an empty last step about half the time, so the release started from silence. Now round.
- Mac: same fix in lhs_model.lua band_voices.

## v76 (9 Nov)
- New loudness shape Reverse: exp rise to a peak (at 0.9), then a steep damped log drop to silence. Drag the peak to move the drop. Ending at silence means the sound release is silent too (no tail). Mac: same shape added to lhs_env.lua.

## v77 (10 Nov)
- Play stopped after ~1-5 s with "The iPad had stopped the sound": the v72 stuck-clock check counted ONE screen frame with an unchanged ac.currentTime as stopped; the iPad clock moves in chunks. Now stopped = no movement for 1.5 s. Mac: n/a (REAPER plays).

## v78 (10 Nov)
- Terminology: "unit" is now "object" on the interface and "sound object" in help and docs (after Schaeffer, objet sonore). Code identifiers, data keys (unit_library, envTarget unit, side tab id) unchanged.
- Help window: search box; every typed word must match an entry; Esc clears.
- v79: "a object" -> "an object". Manuals (Manual/*.md, Interim Manual) now say "sound object" (UI labels Object). Mac Score Tool lib UI strings renamed the same way (data keys kept); not yet run in REAPER. Backups of the pre-rename md and lua in the session scratchpad only.

## v80 (10 Nov)
- LFO on any lane (loudness, one note, pan, spread, modulation): Shape ▾ › LFO. It is ONE envelope written as points onto the lane (REAPER automation-item style), drawn with an LFO box. Settings kept in s.lane_lfo[vol|note:<key>|pan|spread] or mods[i].lfo {shape, baseline 0-1, amp 0-1, rate, phase, skews, tilt, pw, seed, range, edge, under (lane before), gen (last section)}. regenLaneLfo writes points; lfoBase restores the drawn lane; Remove restores, Keep as points drops the settings. Older s.lfo (loudness, live) still plays and edits in the same panel.
- Section moved into the LFO row; LFO out of Edit ▾. Reset renamed Clear. No "tremolo" wording; LFO presets renamed (Sine 4 Hz etc).
- Mac parity TODO: Score Tool reads the points, so it sounds the same; its UI needs Shape › LFO per lane, the box, Clear wording, and keeping lane_lfo/mods[i].lfo on save.

## v81 (10 Nov)
- Tremolo shape removed from the shape list (iPad and Mac lhs_env.lua); LFO does it. Mac LFO preset names and tips now match the iPad (no "tremolo"). Docs: ping-pong pan now via Pan lane LFO.

## v82 (10 Nov)
- Lane marks (L P S 1-3) sit just above where the object starts (its top at its first moment: band points + width with edge fade, cloud hi edge, pulse path, line) and scroll off with it (clipped to the plot; no longer pinned to the left edge). Mac parity: same rule when marks are added there.

## v83 (10 Nov)
- Move to layer… / Copy to layer… (K / ⇧K; buttons in the Object panel and the multi-selection panel). Opens a layer chooser (ask bar); same time and pitch, everything kept (cloneList: new ids, groups re-keyed). Mac parity TODO.

## v84 (10 Nov)
- Object panel buttons in side-by-side pairs: Duplicate|Split, Copy|Save to library, Move|Copy to layer, Paste|Library; Shape: Converge|Fan out, Emerge|Block.
- v85: Shape · Block buttons back to the v83 layout (pairs were unreadable on the iPad).
- v86: Shape · Fan in (mirror of Fan out: wide at the start, back to the drawn range at the end). Mac: "Fan in" outline added in lhs_app.lua (mirror of the Mac Fan out, which differs from the iPad one).

## v87 (10 Nov)
- ▶ Object / ⇧Space: the play head now moves across the object (and across a multi-selection) while it plays alone (followObjHead; same latency correction as Play). Button text while playing: ■ Object (was ■ Unit).

## iPad-only pipeline (10 Nov)
- The app source now lives in GitHub L-SIAL/spectral-score (public; user chose it): ipad/ (one html), standalone/build.py, CLAUDE.md, HANDOFF.md copy, PARITY_TODO.md, .github/workflows/deploy.yml (build + deploy-pages on push to main).
- Mac checkout: LH_Palette_Handoff/repo. standalone/publish.py now copies the newest ipad html into repo/ and pushes; if the iPad made a newer version it copies it down to ipad/ (+ *.from-ipad notes) and stops. Old script kept as publish_before_v88.py; the old standalone/site checkout is no longer used.
- Pages source must be "GitHub Actions" (Settings › Pages), set by the user.

## v88 (10 Nov, made on the iPad via Claude Code + GitHub)
- Help window title is now "Help – Spectral Score". First iPad round trip: PR #1 merged, workflow deployed. Pages source switched to GitHub Actions by the user; old built copy removed from the repo root.

## v89 (10 Nov)
- Help: new section "Changing the app from the iPad" (the 9-step round trip). Same steps in the repo README.md.

## v90 (11 Nov)
- Settings › Score › Listening: Stereo (speakers) | Binaural 3D (headphones); saved as localStorage lhSpatMode. Binaural = one HRTF PannerNode per voice (schedule(): pn.hrtf), position on a unit circle (x = sin az, z = -cos az) automated with setValueCurveAtTime, so each voice follows its full Space azimuth (applySpace now also keeps x.az in degrees, extended through release tails). Voices without a Space lane: asin(stereo pan), in front. Stereo sources (Breath) summed ×0.5 into the panner. Level BIN_K 0.785 = matched to the stereo panner (sine 440 and Breath within 0.5 dB). Binaural voices cost +2 and the voice limit is halved (playLim). Test hook __lh.spatTest(mode, azAt(u), secs).
- Mac parity: binaural monitoring in REAPER (8-ch synth output → binaural decoder, or an LH binaural output mode); to discuss.

## v91 (11 Nov)
- Rotation up to ±64 turns across the object (was ±8); the Settings slider is cubic (slToRot / rotToSl) so small values stay easy.
- Rotation lane (lane button "Rotation", mark R, stack row, LFO key 'rot'): s.rot_env = speed over the object, 0.5 still, 1 = space.rotate, 0 = the same backwards. Angle = 360 × rotate × running integral of (2·speed − 1) (rotTurnsFn, 512 steps); a flat top lane = the old steady rotation; rotate 0 with a lane = 1 turn. Split keeps rot_env.
- Mac (same day, NOT yet run in REAPER): lhs_env.lua SPACE_DEFS.rot + lane menu / stack / removal; lhs_model.lua space_fns integrates rot_env the same way; lhs_app.lua Rotation slider ±64 cubic; lhs_edit.lua split keeps rot_env. Backup: script backups/LH Score Tool lib before rotation lane 2026-11-11.
