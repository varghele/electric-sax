# Measuring the parts

Goal: replace every guess in `cad/components/catalog.yaml` with a caliper reading, then design the electronics sled against real numbers.

## Workflow

1. Measure a part (calipers, mm, one decimal is plenty).
2. In `catalog.yaml`: update `dims`, set `confidence` to `measured`, add `measured_on: YYYY-MM-DD`, remove what you covered from `to_measure`.
3. If the part has a rough shape worth modelling (Pi stack, H2MIDI with plugs, charger), drop a simple STEP/STL into `cad/components/models/<part-id>.stl` – a box-and-cylinder sketch is enough. Note the origin you used in the catalog entry.
4. Photos go to `docs/photos/<part-id>_*.jpg` – a ruler in the shot helps.
5. Run `python build.py --fit` in `cad/` and commit catalog + report together.

## Priority list

### 1. Blocks the electronics sled
| Part | What |
|---|---|
| Pi stack (Pi 5 + Active Cooler + 16 mm riser + DAC Pro, assembled) | Total height, footprint incl. overhanging jacks, where cables leave (USB, P6, power pins) |
| H2MIDI Pro | Body + clearance for the plugged USB-A, USB-C and DC plugs (plug + bend radius) |
| Keystone 1047 ×2 with cells | Confirm 77.0 × 39.8 × 14.9 and cell protrusion |
| Charger (Adeept MRB045) | Total height incl. USB-C socket, socket centre height above PCB, mounting holes |
| BMS | Height incl. tallest component, pad positions |
| U3V40F9, D36V28F5, INA219, level indicator | Outline + height |

### 2. Blocks the panel parts
| Part | What |
|---|---|
| Hole gauge (print F) | Which toggle hole fits best: 6.2 / 6.4 / 6.7. D-size cutout fits both jacks? Insert hole OK? |
| GQ16F button | Depth behind the panel incl. lugs, lug layout |
| Hicon 3.5 mm jack, MIDI socket | Depth behind the panel incl. solder lugs, flange size |
| WS2812 ring | PCB + LED height, pad positions |

### 3. The instrument (do with the collar fit test H + G)
| What | Why |
|---|---|
| Bottom end OD, length free of keys | Collar clamp |
| OD at 100–130 mm above the bottom, key-free side | Clearance to the leg |
| USB-C port orientation, space for an angled plug | Cable path into the bow |
| Lowest key / guard: height and protrusion | Clearance |
| Thumb rest, strap ring positions | Balance and hand clearance |
| Weight of the assembled bell + electronics on the strap | Balance check (EMEO 1.7 kg + ~0.85 kg) |

## Desk tests before building in (record results in `docs/test-log.md`)

- [ ] H2MIDI on 9 V DC with EMEO on USB-A and Pi on USB-C at the same time: MIDI reaches both DIN and Zynthian.
- [ ] EMEO is recognised by Zynthian as a USB MIDI device ("Arduino").
- [ ] Zynthian, soundcard "IQAudio DAC Pro": clean headphone audio, no crackles.
- [ ] Short press on the J2 button shuts Zynthian down cleanly; press again boots.
- [ ] Pi 5 + DAC + cooler on the D36V50F5 under full Zynthian load: no undervoltage warning (`vcgencmd get_throttled` = 0x0).
- [ ] Button LED brightness with 150 Ω at 5 V.
- [ ] XIAO drives the ring through the 74AHCT125 (firmware `breathe`).
- [ ] Pack runtime: practice mode (Pi + Zynthian) and concert mode (H2MIDI + EMEO + ring).
