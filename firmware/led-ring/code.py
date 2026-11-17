# EMEO bell – logo backlight ring (CircuitPython, Seeed XIAO RP2040)
#
# Runs on its own 5 V rail (Pololu D36V28F5, "LED" toggle), independent of the Pi, so the logo
# glows at concerts with the Pi switched off.
#
# Wiring (see docs/wiring.md):
#   XIAO D10 --> 74AHCT125 (VCC 5 V, OE tied to GND) --> 330 ohm --> ring DIN
#   ring 5V/GND from the LED rail, 1000 uF across it at the ring.
#   XIAO 5V pin fed through a 1N5817 Schottky (so plugging in USB never back-feeds the rail).
#
# Status: written before the hardware arrived – UNTESTED. Install CircuitPython for the XIAO RP2040,
# copy neopixel.mpy + adafruit_pixelbuf.mpy from the matching library bundle into /lib, then copy
# this file as code.py.

import time, math
import board, neopixel

# ---------------- settings ----------------
PIN = board.D10
NUM_PIXELS = 16
MODE = "breathe"          # "solid" | "breathe" | "spin"
COLOR = (40, 255, 120)    # matches the green button ring; change to your logo colour
MAX_BRIGHTNESS = 0.35     # hard cap: 16 LEDs at full white draw ~1 A and run hot behind 1 mm of plastic
BREATHE_PERIOD_S = 6.0    # one slow in/out cycle
BREATHE_FLOOR = 0.25      # never fully dark while breathing
SPIN_PERIOD_S = 4.0
FPS = 50

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=MAX_BRIGHTNESS, auto_write=False)


def scaled(color, k):
    return tuple(int(c * k) for c in color)


def frame_solid(t):
    pixels.fill(COLOR)


def frame_breathe(t):
    # cosine ease: smooth at both ends, nothing flickers on stage
    phase = (1 - math.cos(2 * math.pi * t / BREATHE_PERIOD_S)) / 2
    pixels.fill(scaled(COLOR, BREATHE_FLOOR + (1 - BREATHE_FLOOR) * phase))


def frame_spin(t):
    head = (t / SPIN_PERIOD_S * NUM_PIXELS) % NUM_PIXELS
    for i in range(NUM_PIXELS):
        d = (i - head) % NUM_PIXELS                   # distance behind the head
        pixels[i] = scaled(COLOR, max(0.08, 1 - d / 6))


FRAMES = {"solid": frame_solid, "breathe": frame_breathe, "spin": frame_spin}
draw = FRAMES[MODE]

# soft start so the 1000 uF cap and the rail don't see a step load
for k in range(1, 21):
    pixels.brightness = MAX_BRIGHTNESS * k / 20
    draw(0); pixels.show(); time.sleep(0.02)

t0 = time.monotonic()
while True:
    draw(time.monotonic() - t0)
    pixels.show()
    time.sleep(1 / FPS)
