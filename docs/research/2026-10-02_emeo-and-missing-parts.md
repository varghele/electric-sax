# EMEO facts and missing parts

> Research snapshot produced with Claude in Chrome, Oct 2026. Prices/stock are dated; decisions taken from it are in docs/decisions.md and docs/bom.md (some items here were later replaced).

All five missing parts can go on your existing orders: the extender kit (which brings its own standoffs) and the level shifter on Amazon, the diode and a different pushbutton at Conrad. For the EMEO, I found weight, length, USB type and neck fixing; most of the fine mechanical dimensions aren't published anywhere I could reach. Nothing was logged into, added to a cart or bought.

Confidence labels: DS = datasheet or manual, PP = product page, Photo = my estimate from product photos, Rev = review or forum, Unclear.

Part 1 – Missing parts
#	Product	Shop	Price	Stock	Link	Key specs
1 + 2	DSLRKIT GPIO riser kit, 8.5 / 11 / 13.5 / 16 mm	Amazon (shipped by Amazon)	€12.50	17 in stock, Mon 5 Oct	B0F1F8PXPP	Each height comes with a 2×20 GPIO riser, a 2×2 PoE riser, 4× M2.5 brass male-female standoffs and 4 nuts (PP). The 16 mm set's standoffs look about 16 mm long (Photo). Pin length and total height not stated (Unclear)
2 (backup)	YOKIVE M2.5 × 16 mm + 6 mm brass standoffs, male-female, 20 pcs	Amazon	€5.19	Mon 5 Oct	B0BWXJYSCG	16 mm body + 6 mm thread (PP). Only needed if the kit's standoffs turn out shorter
3	PENGLIN SN74AHCT125N DIP-14, 10 pcs	Amazon	€9.49	Mon 5 Oct	B0GK731LKJ	AHCT version (PP). ⚠ 3.9★; no listing guarantees genuine TI chips. For a sure genuine part, try Reichelt or Mouser (I didn't check them)
4	Taiwan Semiconductor 1N5817, DO-41	Conrad	€3.00 (minimum order 30 × €0.10)	2290 in stock, Mon 5 Oct	2994466	1 A / 20 V, forward voltage 0.45 V (PP)
4 (alt)	Vishay SS14-E3/61T, SMA	Conrad	€0.04, minimum 1	1277 in stock, clearance	596519	40 V / 1 A, surface-mount
5	TRU GQ16F-10E/J/G/12V	Conrad	€8.99	159 in stock	701880	Normally open, green ring, 16 mm hole, IP65. LED forward voltage 2.8 V / 20 mA (PP). The datasheet says "12 V (with external resistor 1 kΩ)", so there's no built-in resistor and it should run on 5 V with a series resistor (my reading). Max panel thickness: the product page says 10 mm; the datasheet says both "10 MAX" and "no more than 6 mm" (Unclear). Depth and pin layout: not found
5 (fallback)	Fabuletta 16 mm, green, LED 3–6 V	Amazon, shipped by the seller, not Amazon	€6.09 + €8.99 shipping	16–22 Oct	B0H4VL99DT	"3-6V/G" printed on the body (Photo). NO + NC contacts, 2.8 mm flat tabs, 16 mm hole, 35 mm overall length (PP). Probably 5 tabs: C / NO / NC / + / − (Photo). Panel thickness and pin markings: not found
Extender and standoffs (items 1–2): Botland and Conrad have no 16 mm extender sold on its own. Botland only includes one inside the official Raspberry Pi SSD and AI HAT+ kits. Neither shop has M2.5 × 16 mm standoffs either.
Level shifter (item 3): neither Botland nor conrad.de has the 74AHCT125. Conrad.at lists the TI part as 1016253.
Pushbutton (item 5): no shop has one actually rated 3–6 V or 5 V that Amazon ships.
The Conrad 701880 above is the better bet. I'd swap it in for the /A version (2357042) you planned to order, whose datasheet only says "12 V".
For 5 V: about 110 Ω gives 20 mA, or 220 Ω gives 10 mA (my calculation). The 330 Ω resistor you ordered gives about 7 mA, which should be visible but dim.

Updated order totals: Amazon about €123.77 and Conrad about €112.59. Both stay above their free-shipping thresholds.

Part 2 – EMEO

The official site is now emeo.music; emeo.com didn't load. There are two models, MK1 (original) and MS (newer). Sources: MK1 specs, MS specs, MS manual, MK1 manual, FAQ.

Weight: 1.7 kg for both models (PP, also Thomann). Centre of gravity: not found.
Length: 500 mm. It's not stated whether that includes the neck (PP). Case: 59 × 17 × 15 cm. Not found: tube diameters, and the lowest key's position and how far it sticks out.
USB port: USB-C, on the bottom cap (DS).
On the MS, the bottom cap also has the 3.5 mm headphone jack, power button, LEDs, reset button and drain hole.
Cables:
MK1 manual: "USB Type-A to Type-C cables only. USB-C to USB-C cables are not supported."
MS manual: recommends a USB-C to USB-C data cable.
Not found: which way the port faces relative to the keys, and whether an angled plug fits.
Power:
USB current draw: not found.
It has its own battery and turns on automatically when connected (DS). Charges at 5 V, 15 W max. Battery life up to 7 h on Bluetooth MIDI, 4 h standalone (MS).
The manual warns some iPhones and iPads may not give enough power and suggests a camera adapter with external power (DS). The H2MIDI Pro's host port supplies up to 500 mA, so that warning could apply to it too (my inference).
EMEO only mentions the CME WIDI Uhost. Nothing found specifically on the H2MIDI Pro or other USB-host boxes.
Class compliance: very likely, but inferred rather than stated.
It shows up as "Arduino MKR WiFi 1010" (MS) or "Arduino" (MK1). The manuals mention no driver and say it works with any DAW on Mac and Windows (DS + inference).
Linux / Raspberry Pi: no reports found, good or bad.
Both models also have Bluetooth MIDI.
Settings and firmware go through the EMEO Connect web app: Chrome or Edge only, over a cable. So you'd need a computer for that, not the Pi.
Neck: held by friction with O-rings, no screw. The manual says to "gently push it in while turning it" (DS). The FAQ recommends 12 mm / 2 mm O-rings, which points to a narrow EMEO-specific tenon rather than a standard alto neck (inference). Receiver inner diameter: not found.
Strap ring / thumb rest: a neck strap is included. Position of the strap ring and thumb rest, and any limit on added weight: not found. A Sax on the Web thread called "EMEO thumb pain" exists, but it was blocked to me.
Couldn't find
Extender kit: pin length and total height, and the exact standoff length.
74AHCT125: a listing that guarantees genuine TI.
Pushbuttons: pin layout and depth behind the panel for both the Conrad and Amazon buttons. The Conrad panel-thickness figures contradict each other.
EMEO:
centre of gravity
length without the neck
tube diameters
lowest key position and how far it sticks out
USB port orientation and whether an angled plug fits
USB current draw
behaviour with the H2MIDI Pro
any Linux or Raspberry Pi reports
neck receiver inner diameter
strap ring and thumb rest positions
guidance on added weight

The EMEO manuals contain diagrams I could only read as text. Checking those, or measuring the instrument, would fill most of these gaps.