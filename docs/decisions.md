# Decision log

Why things are the way they are. Add new entries at the bottom; don't rewrite old ones – mark them superseded.

| # | Decision | Reason |
|---|---|---|
| 1 | Bell built around the EMEO's bottom end, clamp remixed from Nerd-Sniped's "EMEO Headless Computer" (Printables 1579980) | Only public geometry that fits the EMEO; OCL v1 allows remixes (same license, no commercial resale). |
| 2 | Concert path is pure MIDI (EMEO → H2MIDI → DIN → midiBeam), Pi is optional | Pi crash can't stop a gig; Pi can be off at concerts. |
| 3 | Pi 5 + Zynthian for practice only, headphones only | No PC powerful enough for SWAM etc.; line out dropped (2 Oct). |
| 4 | Raspberry Pi DAC Pro as sound card | Real headphone amp; Zynthian supports it ("IQAudio DAC Pro"). PCM5102 boards have no headphone amp. |
| 5 | One custom 2S2P 18650 pack instead of power banks | Pi 5 needs 5 V / 3–5 A; power banks drop outputs on renegotiation and auto-shut-off at low load. One charge port. |
| 6 | Cells in Keystone holders, not welded tabs | No soldering on cells, swappable. Printed lid presses cells in so they can't bounce. |
| 7 | Three rails, each with its own toggle: Pi (D36V50F5), MIDI (U3V40F9 9 V), LED/display (D36V28F5) | Independent concert/practice modes; LED ring works without the Pi. |
| 8 | Pi powered through GPIO 5 V with `PSU_MAX_CURRENT=5000`, `POWER_OFF_ON_HALT=1` | No PD negotiation, full USB current, near-zero drain when halted. |
| 9 | LED ring driven by a XIAO RP2040 on the LED rail via 74AHCT125 | Visible at concerts with the Pi off; frees GPIO18 for the DAC; 3.3 V data is out of spec for a 5 V WS2812. |
| 10 | Hexagon design language from the user's S-bow: concave faces, **sharp** edges, corners in the bend plane, smooth round→hex transition | User's own mouthpiece design; chamfers were tried and rejected. |
| 11 | Bell split into 3 shells (A collar+bend, B leg, C bell) with spigots + M3 inserts | Fits the CORE One; serviceable, nothing glued. |
| 12 | Rim has the Ø154 mm pocket for the Waveshare 5" round display; V1 ships a white cover plate with the LED ring behind it | V2 display drops in without reprinting; display is ~€147. |
| 13 | TX02 in a slide-in cradle on the audience side, MIDI socket below it | TX02 is on a 15 cm cable; front (switch, LEDs, knob) stays accessible, battery door on the back reachable by sliding it out. |
| 14 | All panel parts D-size where possible | Owned parts are D-size; robust. |
| 15 | Drain holes at the lowest point of the bend | EMEO bottom cap has a drain hole; condensation must not pool on electronics. |
| 16 | Toggle row gets one 46 × 16 mm pocket instead of 13 mm round counterbores (17 Nov 2026) | Fit check: toggle body diagonal 14.1 mm collided with the 13 mm pockets. |
