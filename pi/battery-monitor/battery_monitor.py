#!/usr/bin/env python3
"""Battery monitor for the EMEO bell – reads the INA219 in the Pi branch over I2C.

The INA219 sits between the pack and the Pi's D36V50F5, so it sees the pack voltage and the Pi
branch current (~0.3-2.5 A at 6-8.4 V). Prints one line per interval (journald picks it up when
run as a service) and logs warnings below WARN_V. It does NOT shut the Pi down by itself: the
D36V50F5 enable divider cuts power in hardware at ~6.4 V. Set SHUTDOWN_V to let the Pi shut down
cleanly a little earlier.

Status: written before the hardware arrived – UNTESTED.
Needs: I2C enabled (dtparam=i2c_arm=on), `pip install smbus2`.
I2C address 0x40 (default, no address jumpers). The DAC Pro's codec uses 0x4c – no conflict.
"""
import argparse, logging, subprocess, sys, time

ADDR = 0x40
REG_CONFIG, REG_SHUNT, REG_BUS = 0x00, 0x01, 0x02
CONFIG = 0x399F          # 32 V bus range, +-320 mV shunt range, 12-bit, continuous (chip default)
SHUNT_OHM = 0.1          # R100 on the CJMCU-219 board

# 2S Li-ion, rough voltage -> state of charge under light load (per pack, 2 cells in series)
SOC_TABLE = [(8.40, 100), (8.20, 90), (8.00, 78), (7.84, 66), (7.70, 54), (7.56, 42),
             (7.44, 30), (7.30, 20), (7.10, 10), (6.80, 4), (6.40, 0)]
WARN_V = 7.0


def read_word(bus, reg):
    raw = bus.read_word_data(ADDR, reg)
    return ((raw << 8) & 0xFF00) | (raw >> 8)        # SMBus is little-endian, INA219 is big-endian


def read(bus):
    bus_raw = read_word(bus, REG_BUS)
    volts = (bus_raw >> 3) * 0.004                   # 4 mV LSB
    shunt_raw = read_word(bus, REG_SHUNT)
    if shunt_raw > 0x7FFF:
        shunt_raw -= 0x10000
    amps = shunt_raw * 10e-6 / SHUNT_OHM             # 10 uV LSB
    return volts, amps


def soc(v):
    if v >= SOC_TABLE[0][0]:
        return 100
    for (v1, p1), (v2, p2) in zip(SOC_TABLE, SOC_TABLE[1:]):
        if v2 <= v <= v1:
            return round(p2 + (p1 - p2) * (v - v2) / (v1 - v2))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--bus', type=int, default=1)
    ap.add_argument('--interval', type=float, default=30.0, help='seconds between readings')
    ap.add_argument('--once', action='store_true', help='print one reading and exit')
    ap.add_argument('--shutdown-v', type=float, default=None,
                    help='clean shutdown when the pack stays below this voltage for 3 readings (e.g. 6.6)')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        from smbus2 import SMBus
    except ImportError:
        sys.exit('smbus2 missing: pip install smbus2')
    low_count = 0
    with SMBus(a.bus) as bus:
        bus.write_word_data(ADDR, REG_CONFIG, ((CONFIG & 0xFF) << 8) | (CONFIG >> 8))
        while True:
            v, i = read(bus)
            line = f'pack {v:5.2f} V  {soc(v):3d} %  pi-branch {i:5.2f} A  {v*i:5.1f} W'
            (logging.warning if v < WARN_V else logging.info)(line + ('  LOW' if v < WARN_V else ''))
            if a.once:
                return
            if a.shutdown_v is not None:
                low_count = low_count + 1 if v < a.shutdown_v else 0
                if low_count >= 3:
                    logging.warning('pack below %.2f V – shutting down', a.shutdown_v)
                    subprocess.run(['systemctl', 'poweroff'])
                    return
            time.sleep(a.interval)


if __name__ == '__main__':
    main()
