# Parts sourcing across shops

> Research snapshot produced with Claude in Chrome, Oct 2026. Prices/stock are dated; decisions taken from it are in docs/decisions.md and docs/bom.md (some items here were later replaced).

You can buy all 25 items from three shops: Conrad, Botland and Amazon.de. Each order is above its free-shipping threshold, so the total is about €315.57 with no shipping cost. Nothing was logged into, added to a cart or bought. Prices and stock are as shown on 1 Oct 2026.

Keystone 1047: each cell has its own contacts. The datasheet shows 4 solder lugs, 2 per cell, with the cells' polarity reversed against each other. Nothing connects the two cells inside the holder, so you wire series or parallel yourself. Size is 77.0 × 39.8 × 14.9 mm, with two Ø3.18 mm mounting holes 55.25 mm apart.

Why these three shops: Conrad is the only one with the Samsung 35E cells and the Keystone holder. Botland has all three Pololu boards (Berrybase has only the D36V50F5, and Amazon charges €47–86 each). The 2S BMS, charger and battery indicator are only on Amazon. Berrybase isn't needed. As a fallback it has a 13.3 mm header (€2.20) and the D36V50F5 (€34.95).

"sub" means a substitute that meets your spec; ⚠ means something to check before ordering.

#	Product	Shop	Price	Stock / delivery	Link	Key specs
1	Samsung INR18650-35E, flat top, no tabs [EXACT]	Conrad	4×5.99 = 23.96	1740 in stock, delivery Mon 5 Oct	1499572	3450 mAh, sold by Conrad
2	Keystone 1047 [EXACT]	Conrad	2×11.99 = 23.98	⚠ only 18 in stock, Mon 5 Oct	1555500	4 lugs, cells wired separately (see above)
3	Pololu D36V50F5 (#4091) [EXACT]	Botland	33.00	ships within 24 h	link	Botland's title says "8A", but #4091 is the right part
4	Pololu D36V28F5 (#3782) [EXACT]	Botland	17.90	24 h	link	20×18 mm
5	Pololu U3V40F9 (#4015) [EXACT]	Botland	8.50	24 h	link	9 V / 3.5 A
6	Raspberry Pi DAC Pro (IQaudio) [EXACT]	Botland	26.90	24 h	link	
7	Raspberry Pi 5 Active Cooler [EXACT]	Botland	5.50	24 h	link	
8	INA219 CJMCU-219, pack of 6 (sub)	Amazon	9.99	shipped by Amazon, ~Mon 5 Oct	B0DDPXD45M	I²C, 0–26 V bus. The single Adafruit 904 at Botland is €13.90
9	2×20 stacking header, long pins (sub)	Botland	1.50	24 h	link	⚠ 12 mm pins, not 13 mm
10	M2.5 brass standoff kit, 320 pcs (sub)	Amazon	16.99	shipped by Amazon	B09YLWJPD7	Female-female 6/10/15/20 mm, male-female 6/10/15/20 mm, plus screws and nuts
11	SanDisk Ultra microSDHC 32 GB A1 (sub)	Conrad	14.99	3849 in stock	2336835	A1, U1, includes SD adapter
12	Seeed XIAO RP2040	Botland	4.50	24 h	link	
13	TRU Components GQ16F-10E/J/G/12V/A (sub)	Conrad	8.49	431 in stock	2357042	16 mm metal, momentary, NO, green ring, IP65. ⚠ The LED is 12 V, so from 5 V or 3.3 V it needs its own resistor. I found no 5 V version
14	TRU TC-9218544 mini toggle switch, ON-ON (sub)	Conrad	3×0.95 = 2.85	over 23k in stock	2304636	SPDT ON-ON, solder lugs. ⚠ The listing gives a 6.6 mm mounting hole
15	TRU TC-Mini FK1 inline holder + 7× MTA 5 A mini fuses (sub)	Conrad	2.79 + 1.68 = 4.47	in stock	holder 1587910 · fuses 849464	Both mini blade size. The holder is for 4 mm² wire. ⚠ It's unclear whether it comes with wire attached
16	ESKA FRX050-60F PTC (sub)	Conrad	7×0.50 = 3.50 (minimum 7)	297 in stock	524823	0.5 A hold, 60 V, radial
17	Reely XT30U, 3 male + 3 female (sub)	Conrad	6×1.79 = 10.74	over 1000 in stock	male 2206368 · female 2206369	Solder type, gold plated. No pair packs at Conrad
18	2S BMS "Balance Version", 5 pcs (sub)	Amazon	17.43	shipped by Amazon, ~Tue 6 Oct	B07T2WKQSQ	20 A continuous, 48 × 20 × 3.4 mm. ⚠ The B−/BM/B+ pad names aren't stated; check the photos
19	Adeept USB-C 2S charger, 2 pcs (sub)	Amazon	9.99	shipped by Amazon	B0BWTK7SVN	5 V USB-C input (3–6 V), charges to 8.4 V at about 1.1 A, charge-only. ⚠ Listed as 40 × 20 × 2 mm (2 mm seems too thin); USB-C position not stated
20	2S 8.4 V level indicator with push button, 5 pcs (sub)	Amazon	13.40	shipped by Amazon, ~Thu 8 Oct	B0CHRHYMS5	5 LEDs. ⚠ No ratings yet
21	WS2812 ring, 16 LEDs, 44 mm (sub)	Botland	6.90	24 h	link	Outer diameter 44 mm. ⚠ Inner diameter not stated; probably about 31–32 mm. If you need confirmed dimensions, the Adafruit 1463 at Conrad (€23.99) is 44.5 / 31.75 mm
22	ruthex RX-M3x5.7, 100 pcs (sub)	Conrad	9.49	149 in stock	3398923	Outer diameter 4.6 mm, length 5.7 mm, 4.0 mm hole (from the ruthex datasheet)
23	TOOLCRAFT screws and nuts (sub)	Conrad	3.71	in stock	e.g. 814156	M3×20 DIN 912 (814156, 7 pcs), M3×10 countersunk DIN 965 Torx (889786, 10 pcs), M3×8 DIN 912 (888736, 15 pcs), M3×10 DIN 912 (888738, 10 pcs), M3 nuts (888118, 10 pcs)
24	330 Ω metal film + Panasonic 1000 µF/10 V	Conrad	0.01 + 2.90 (minimum 5)	in stock	1583963 · 1475960	Capacitor is 10 mm diameter
25	ENERJOUR silicone wire, 20 AWG 6×7 m + 24 AWG 6×9 m (sub)	Amazon	16.99 + 16.99	shipped by Amazon	20 AWG · 24 AWG	Each set has red, black, white, blue, green and yellow

Per shop:

Shop	Items	Subtotal	Shipping
Conrad	1, 2, 11, 13–17, 22–24	€109.09	€0 (free from €100; otherwise €4.95)
Botland	3–7, 9, 12, 21	€104.70	€0 (free from €100; otherwise €4.99)
Amazon.de (all shipped by Amazon)	8, 10, 18–20, 25	€101.78	€0 (free from €49; otherwise €3.99)
Total		€315.57	€0

Before ordering:

Botland is only €4.70 over its free-shipping limit. If anything there sells out, add the Adafruit INA219 (€13.90) to stay above €100.
Conrad only has 18 Keystone holders in stock.
The Amazon shipping cost of €3.99 below €49 comes from press reports, not Amazon's own pages. It doesn't matter here because the order is above €49.

Sources: Keystone 1047 product page, ruthex RX datasheet, Conrad, Botland shipping, Berrybase shipping, techbook.de on Amazon shipping, plus the product links in the table.