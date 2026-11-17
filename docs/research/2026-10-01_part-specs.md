# Technical specs of ordered parts

> Research snapshot produced with Claude in Chrome, Oct 2026. Prices/stock are dated; decisions taken from it are in docs/decisions.md and docs/bom.md (some items here were later replaced).

I couldn't find a 16 mm pushbutton with a green ring and a 5 V LED that Amazon ships itself. Everything else is answered below, with gaps flagged. I checked the Active Cooler and DAC Pro drawings myself in the browser. Nothing was logged into, added to a cart or bought.

Confidence labels:

DS: datasheet or official docs
PP: product page
Photo: my estimate from product photos
3rd: another seller's listing or a forum post
Unclear
A) Missing part

1. 16 mm button, green ring, 5 V LED, shipped by Amazon: not found. About 8 searches and 10 listings checked. Every Amazon-shipped version has a 12 V or 12–24 V LED.

GUUZI B097MNDK6G, €8.99, shipped by Amazon. The variant selector has no 5 V option (12/24/230 V only). Specs (PP):
16 mm hole, max panel thickness 11 mm, 19 mm head.
1× NO contact, 4 pins, plug-on cable included.
Closest 5 V option, not shipped by Amazon: B0H4VL99DT, green, LED 3–6 V DC. €6.09 + €8.99 shipping, delivery 16–22 Oct.
16 mm hole, NO + NC, 2.8 mm flat tabs (PP).
"Length 35 mm" (PP), but it doesn't say whether that includes the lugs.
Max panel thickness and a pin map: not found.
Photo: 5 tabs on the base, which fits the usual C / NO / NC / LED+ / LED− layout. Unclear.
Workaround: keep the 12 V Conrad button. Many 12 V ring LEDs already have a series resistor built in, so they glow dimly or not at all at 5 V. You'd need to test it.
B) Ordered parts

2. Adeept 2S charger (B0BWTK7SVN, board "MRB045")

Size: 37 × 17 mm including the USB-C socket (dimension image, PP). Bare PCB about 35.3 mm (Photo).
Total height: not given. A third-party listing of the same board says 6.3 mm (3rd).
USB-C socket: centred on one short edge and overhanging it by about 1.7 mm (Photo).
Mounting holes: 2, at the battery end only. About 1.6–2 mm diameter, about 13.6 mm apart (Photo).
Pads (silkscreen, Photo):
USB end: VIN and GND (small).
Battery end: BAT and GND (large square pads, between the holes).
Underside: solder jumpers OUT 2S/3S/4S and IN 1A/2A/4A, bridged at 2S/2A. Marked "IN 3–6V".
Charging chip: not legible on the photos. A visible "4468" is probably an AO4468 MOSFET.
Electrical (PP): input 3–6 V, 2 A. Charges to 8.4 V at about 1.1 A.
Reviews say it doesn't work with USB-C PD chargers, only plain 5 V ones (3rd).
LEDs: two, marked CR (charging) and OK (full). The CR/OK meanings come from a third-party listing of the same board; colours not confirmed.

3. 2S BMS Balance (B07T2WKQSQ)

Size: 48 × 20 × 3.4 mm (PP).
Pads (Photo):
0V = B−, 8.4V = B+ (opposite corners at one end).
4.2V = BM (small pad on the end edge).
⊖ = P−, ⊕ = P+.
Current (PP): 20 A discharge, 10 A charge continuous. One review reports it cutting out at 4 A.
Cut-off voltages: not on the listing. Other sellers of the same design give:
Overcharge 4.2–4.3 V per cell.
Over-discharge 2.3–2.6 V per cell.
Over-current 25 A.
Sources (3rd): makerselectronics, done.land
Balancing: yes, during charging only (PP). Roughly 100 mA through 43 Ω bleed resistors (3rd, and it matches the resistor values).

4. Botland WS2812 ring, 16 LEDs (link)

Diameters: outer 44 mm, inner 34 mm (PP).
Board thickness and LED height: not given. 5050 LEDs are typically about 1.6 mm tall (general knowledge, not checked for this part).
Back (Photo): silkscreen "CJMCU-2812-16". Six pads in one column near the outer edge, top to bottom: GND, VCC, OUT, then a gap, then IN, VCC, GND.

5. TRU TC-9218544 toggle switch (datasheet, DS)

Thread: M6 × 0.5.
Mounting hole: drawn as Ø6. Print it about 6.2–6.5 mm (my suggestion, not from the datasheet).
Max panel thickness: not stated. The bushing is 8.8 mm tall including the nut, so a thin panel is no problem.
Below the panel:
Body 12.5 × 6.5 × 9.5 mm.
3 lugs, 4 mm long, 4.5 mm pitch.
About 13.5 mm total depth.
Lever: the drawing shows 12.5 mm and the text says 11.3 mm. These conflict.

6. Neutrik NJ3FP6C (drawing, DS)

Cutout: Ø24 mm hole, plus 2× Ø3.4 mm holes on a diagonal, 19 × 24 mm apart (standard D size).
Flange: 26 × 31 mm.
Depth behind the panel: 29 mm.
Max panel thickness: not stated.

7. The 3.5 mm jack at Thomann is not a Neutrik part. It is a Hicon HI-J35SEFD (Sommer Cable's own brand), a 3-pole stereo jack on a D-size flange (Thomann, Sommer).

Cutout: presumably the standard D cutout, but that is inferred from "D-size" (Unclear).
Depth: about 15–20 mm (Photo).
Max panel thickness: not found.

8. Thomann MIDI panel socket (link)

Cutout: the page only says "für D-Norm Löcher", which implies Ø24 mm + 2× M3 at 19 × 24 mm (Unclear).
Photo: D-shaped flange with 2 diagonal holes. A reviewer says the flange is thin sheet metal, though the page says plastic.
Depth: about 20–22 mm including the 5 solder lugs (Photo).
Flange size: not found.

9. TC-Mini FK1 fuse holder (datasheet)

Wire attached: yes, 2 leads of 130 mm each, stripped (DS).
Wire size: the datasheet says 12 AWG (about 3.3 mm²) and the product page says 4 mm². These conflict.
Dimensions: body 54.5 mm long including strain reliefs, about 11 × 11 mm cross-section (DS).

10. CME H2MIDI Pro (manual, DS)

Housing: 75 × 38 × 33 mm.
DC input:
9 V, 500 mA, 5.5/2.1 mm barrel.
Centre negative (pedal-style polarity).
No voltage range given; consumption about 281 mW.
It can also run from USB-C at 5 V.
Port roles are the other way round from what you assumed:
USB-A is the host port for MIDI devices. It supplies up to 5 V / 500 mA to them.
USB-C is the device port to a computer, and also a power input.
Computer and host at the same time: the routing chart sends USB-A traffic to both DIN and USB-C, which implies it works. No sentence says so explicitly, and the manual doesn't say which supply wins when DC and USB-C are both connected.
Routing: set in the HxMIDI Tools app (macOS/Windows/iOS/Android). Settings are saved in the device, with 4 user presets you can switch by button or MIDI. It then runs standalone.
C) Raspberry Pi 5 stack

11. Active Cooler (drawing, DS, checked visually)

Size: footprint 63.5 × 42.5 mm, fan 30 × 30 mm, overall height 13.7 mm. The 13.7 mm seems to include the push-pin tips under the plate, so the height above the board is slightly less (Unclear).
Under a standard HAT: a HAT at standard header height doesn't fit.
Recommendation:
The HAT+ spec asks for at least 15 mm spacers, 16 mm ideal (DS).
The Raspberry Pi blog uses "16mm GPIO extenders".
So: 16 mm standoffs plus a 16 mm stacking or extension header. The ~12–13 mm header you ordered is too short.

12. DAC Pro (product brief p.4, DS, checked visually)

Board: 65 × 57 mm, 4× M2.5 holes at 58 × 49 mm.
Jack positions:
The two RCA sockets and the 3.5 mm headphone socket all sit on the long edge opposite the GPIO header and overhang it.
The headphone jack's centre is about 53.2 mm from the left edge; the RCA dimension is 26 mm.
The drawing is a top view, so the exact reference points are approximate.
Jack heights: not given.
Headers (docs, DS):
P1: 0–2 V RMS line out (L, R, 2× GND, plus GPIO27 mute).
P6: headphone signals (1 L, 2 GND, 3 R, 4 GND, 5 detect).
P7 / P9: differential 0–4 V RMS outputs, P7 = left, P9 = right, 3 pins each.
⚠ Conflict on P7: the product brief calls P7 the 0–2 V analogue out, which contradicts the docs. The pin order isn't published, so check the board's silkscreen.
Overlay: dtoverlay=rpi-dacpro.

13. Pi 5 power button and powering via GPIO (docs, DS)

J2 location: between the RTC battery connector and the board edge.
Short press:
When halted or off: boots the Pi.
With a desktop: opens a shutdown dialog.
Without a desktop: clean shutdown. This is systemd-logind HandlePowerKey behaviour (3rd).
Long press: hard power-off.
EEPROM: sudo -E rpi-eeprom-config --edit, then add:
POWER_OFF_ON_HALT=1 with WAKE_ON_GPIO=0. Draw when off drops to about 0.01 W. Caveat from the docs: "may cause problems with some HATs because 5V will still be on".
PSU_MAX_CURRENT=5000. This skips USB-PD negotiation.
Powering through the 5 V GPIO pins: officially supported via the "Power HAT+" concept in the HAT+ spec (DS). Caveats:
At least 3 A at 5.1 V; 5 A strongly recommended.
The supply must only source current and must tolerate USB-C being plugged in at the same time. Backfeed protection is your job.
With no PD negotiation, USB ports are limited to 600 mA unless PSU_MAX_CURRENT=5000 or usb_max_current_enable=1 is set (whitepaper).
That the Pi's input protection is bypassed is my inference, not an official sentence.

14. Zynthian

Pi 5 support: yes. The current stable release is Oram-2511; kit v5.1 supports the Pi 5 (wiki).
Soundcard: there is no "Raspberry Pi DAC Pro" preset in webconf. Choose "IQAudio DAC Pro" (iqaudio-dac, hw:Pro) or "IQAudio DAC+" (from the webconf source code).
Known-good Pi 5 + DAC Pro jack settings (solved forum thread, 3rd): -P 70 -s -S -d alsa -d hw:IQaudIODAC -r 48000 -p 128 -n 2 -o 2 -X raw.
Caution: a July 2026 forum post mentions past IQaudio problems (thread, 3rd).
Clean shutdown from the Pi 5 power button: no Zynthian-specific note found. Zynthian has no desktop, so a press should trigger a normal systemd shutdown, but that's inference; test it.
D) LED controller

15. XIAO RP2040 (wiki, DS)

Board: 21 × 17.8 × 3.5 mm.
5 V pin: labelled 5V, it is VBUS and works as power in or out. It's not documented whether there's a diode to USB. Seeed recommends a Schottky diode on external 5 V to stop backfeed (blog, written for another XIAO).
Data pin: any GPIO works through PIO. D10 (GPIO3) or D0 (GPIO26) is my suggestion, not a Seeed example. The onboard NeoPixel uses GPIO12.
3.3 V logic into a 5 V ring: not within spec. The WS2812B needs at least 0.7 × VDD, which is 3.5 V at 5 V (datasheet). Adafruit says a level shifter is required, e.g. 74AHCT125, plus a 300–500 Ω series resistor and 500–1000 µF across the supply (Überguide). It often works without one, but not reliably.
Could not find
A 5 V green-ring 16 mm button shipped by Amazon (and full dimensions or pin map for the non-Amazon 3–6 V one).
Charger: total height, charging chip, LED colours.
BMS: cut-off voltages from the listing itself (third-party figures only).
Ring: PCB thickness and LED height.
Toggle switch: max panel thickness; lever length is contradictory.
NJ3FP6C: max panel thickness.
Hicon jack and Thomann MIDI socket: any drawing (cutout inferred, depth from photos only).
Fuse holder: wire size is contradictory.
H2MIDI Pro: DC voltage range, explicit confirmation that USB-A and USB-C work at the same time, which supply wins.
DAC Pro: jack heights and P7/P9 pin order.
Zynthian: any Pi 5 power-button note.
XIAO: whether there's a diode on the 5V pin.