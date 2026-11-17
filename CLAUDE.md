# CLAUDE.md – electric-sax

Context for Claude (and humans) working in this repo. Read this first, then `docs/decisions.md`.

## What this is

A 3D-printed bell for an **EMEO MK1** digital sax (owner plays it on stage). The bell houses: a CME H2MIDI Pro (MIDI split), a Raspberry Pi 5 + DAC Pro running Zynthian (practice, headphones only), a 2S2P 18650 pack with three switched rails, a midiBeam TX02 MIDI transmitter in an outside cradle, and a logo LED ring driven by a XIAO RP2040. Design language: the owner's printed **S-bow** (concave hexagon, sharp edges). Printer: Prusa CORE One, ASA.

Full rationale: `docs/decisions.md`. Electrical design: `docs/architecture.md`. Parts: `docs/bom.md`.

## Hard rules

1. **Never invent dimensions.** Every bought part's geometry lives in `cad/components/catalog.yaml` with a `confidence` level. If a number isn't there, say so and add it to `to_measure` – don't guess silently. Only `measured` values should drive final CAD; flag anything printed against `photo`/`unknown` values.
2. **Don't silently change settled decisions** (hexagon with sharp edges, concert path bypasses the Pi, three independent rails, MIDI toggle before the 9 V boost, D-size panel parts, drain holes). Propose changes and log them in `docs/decisions.md`.
3. **Licensing:** parts A, G, H contain Nerd-Sniped geometry (OCL v1, no commercial use). Keep the attribution in `cad/vendor/nerd-sniped/README.md` and `LICENSES.md`.
4. **Safety:** Li-ion pack. Keep the BMS, 5 A fuse and XT30 disconnect in every revision; the battery compartment stays separated from the Pi's heat. Never power the Pi from GPIO 5 V and USB-C at the same time.
5. Build output (`cad/build/`) is generated – don't commit it. Release meshes go into GitHub Releases.
6. Everything in `pi/` and `firmware/` was written before the hardware arrived and is **untested** until `docs/test-log.md` says otherwise.

## CAD conventions

- Units **mm**. Global frame = Nerd-Sniped's frame: **Y up along the EMEO**, EMEO axis at x=0, z=0, bend plane = XY, the bell sweeps toward −X.
- `esax/geom.py`: centreline path (`PTS`, `TAN`, arc length `DIST`), cross-section profile (`profile(d)` → apothem, concavity, hex blend), sweep/loft helpers, manifold helpers (`box`, `cyl`, `placed`).
- `esax/bell.py`: `build()` returns every printable part as a `manifold3d.Manifold`. Panel features are placed with `(phi, y, v)`: phi 90 = player side (+z), 270 = audience side (−z); y = height on the straight leg; v = offset across the face.
- `components/layout.yaml` mirrors the panel positions in `bell.py`. **When you move a hole in `bell.py`, move the entry in `layout.yaml` too**, then run `python build.py --fit`.
- Keep parts watertight: check `report.json` (`status` must be `Error.NoError`, volumes plausible). Before claiming a geometry change works, rebuild and render or section it and look.
- Max part size: 250 × 220 × 270 mm (CORE One).

## Commands

```bash
cd cad
pip install -r requirements.txt
python build.py                 # all parts -> build/, report.json
python build.py --fit           # + component clearance check (fit_report.txt, proxies.stl)
python build.py --viewer        # + build/viewer.html (three.js, self-contained)
python build.py --only F_hole_gauge
```

Baseline volumes (cm³) after the 17 Nov 2026 import – a change elsewhere shouldn't move these unexpectedly:
A 165.3 · B 123.3 · C 159.1 · D 58.2 · E 14.9 · F 16.4 · H 35.5

## Parts list (V1)

| ID | Part | Status |
|---|---|---|
| A | Collar + U-bend (incl. Nerd-Sniped socket) | designed |
| B | Straight leg with control pads | designed |
| C | Flare + rim, Ø154 screen pocket | designed |
| D | Cover plate with LED ring seat (print white) | designed |
| E | TX02 cradle | designed |
| F | Hole gauge | designed – print first |
| G | Clamp half (Nerd-Sniped, unchanged) | vendored |
| H | Collar fit test | designed – print second |
| – | Electronics sled (Pi stack, battery holders, BMS, converters, charger, H2MIDI, XIAO) | **not started – needs measurements** |
| – | Battery retaining lid | not started |

## Current task queue

1. Owner measures parts → `catalog.yaml` (see `docs/measurements.md`). Owner may add rough STL/STEP sketches to `cad/components/models/`.
2. Desk tests (list in `docs/measurements.md`) → `docs/test-log.md`.
3. Design the electronics sled: add `internal:` entries to `layout.yaml`, new module `esax/sled.py`, mounting bosses in the shells; keep heavy parts (cells) low in the bend; cable paths; airflow from the low intake vents past the Pi to the high exhaust vents.
4. Battery compartment lid that presses the cells into the Keystone holders.
5. Logo on the cover plate (owner supplies SVG).
6. Firmware/Pi code once hardware is on the desk.
7. V2: Waveshare 5" round display + Pi Zero 2 W on the LED rail.

## Open questions

- D36V50F5 / D36V28F5 EN threshold → resistor divider for a ~6.4 V undervoltage cutoff (check the Pololu datasheets).
- Does the H2MIDI keep both USB-C (to Pi) and USB-A host working while on 9 V DC? (desk test)
- Exact position/orientation of the EMEO's USB-C on the bottom cap and room for an angled plug.
- Which toggle hole size fits (6.2 / 6.4 / 6.7) – from the hole gauge.
- Weight balance on the strap with ~0.85 kg added at the bottom.

## Research archive

`docs/research/` holds the web research done with Claude in Chrome (Oct 2026): sourcing, part specs, EMEO facts. Treat it as a snapshot: prices and stock change, and confidence labels in those notes still apply.
