# LED ring firmware (Seeed XIAO RP2040, CircuitPython)

Lights the 16-LED WS2812 ring behind the logo on the cover plate. Runs on the LED rail, independent of the Pi.

## Install

1. Hold BOOT while plugging the XIAO into USB, drop the CircuitPython `.uf2` for "Seeed XIAO RP2040" onto the drive.
2. From the CircuitPython library bundle matching that version, copy `neopixel.mpy` and `adafruit_pixelbuf.mpy` to `CIRCUITPY/lib/`.
3. Copy `code.py` to `CIRCUITPY/`.

Settings are at the top of `code.py`: mode (`solid` / `breathe` / `spin`), colour, brightness cap.

**Unplug the LED rail toggle or use the 1N5817 path when programming over USB.** See `docs/architecture.md`.

## Ideas for later

- React to MIDI (note velocity → brightness) via a DIN thru tap or a USB connection.
- V2: the Zero 2 W drives the round display; the XIAO could stay for the ring.
