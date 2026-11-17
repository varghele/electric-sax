# Printing and assembly (V1)

Printer: Prusa CORE One (250 × 220 × 270 mm), every part fits. Material: **ASA** (stays stable on a hot stage / in a car), cover plate D in **white/natural** so the LED ring glows through.

## Parts (build with `cd cad && python build.py`)

| File | Part | Notes |
|---|---|---|
| A_collar_bow | Collar + U-bend | Contains Nerd-Sniped's clamp socket (OCL v1 remix), inserts re-bored for M3. Supports in the bend. Two drain holes at the lowest point. |
| B_leg_controls | Straight leg, both control pads | Player side: 3 toggles (MIDI / Pi / LED), Pi button, headphone jack (D-size), USB-C charge slot. Audience side: MIDI socket (D-size), 2 inserts for the TX02 cradle. Vents. |
| C_bell_rim | Flare + rim with Ø154 mm screen pocket | Print rim-down with organic supports. |
| D_cover_plate | V1 cover for the screen pocket | LED ring seat behind a 1 mm skin. Add your logo in the slicer. |
| E_tx02_cradle | Slide-in cradle for the midiBeam TX02 | Print flat. |
| F_hole_gauge | Test coupon | **Print first.** Toggle 6.2 / 6.4 / 6.7, button 16.2, D-size 24.2 + 2× 3.4, insert 4.0, USB-C slot. |
| G_clamp_half_NerdSniped | Removable clamp half | Unchanged original. |
| H_collar_fit_test | Socket region of A only (~36 cm³) | **Print second.** Fit on the EMEO with G before printing A. |

## Order

1. **F** – check every hole against the real part; report the best toggle size.
2. **H + G** on the EMEO: seats without wobble, clamp closes with 3× M3×20 without force, USB-C reachable with the A-to-C plug, nothing hits a key or the thumb rest.
3. **A, B, C, D, E**.

## Hardware

- A–B and B–C joints: 6× ruthex M3 × 5.7 insert (4.0 mm holes) + 6× M3 × 8
- Clamp G → A: 3× insert + 3× M3 × 20
- Cover plate: 4× insert (in D) + 4× M3 × 8 from inside through the rim ledge
- TX02 cradle: 2× insert (in B) + 2× M3 × 10 countersunk
- MIDI socket, headphone jack: 2× M3 × 10 + nuts each

## Weight

Shell ≈ 450 g in ASA at 2.2 mm walls. Electronics ≈ 400 g. With the EMEO (1.7 kg) ≈ 2.5 kg – about an alto sax. If it's too heavy, drop `wall` in `cad/esax/geom.py` to 1.8.
