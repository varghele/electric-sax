# Raspberry Pi 5 – Zynthian practice synth

Practice only: the Pi is switched off at concerts (MIDI to the stage PC bypasses it).

## Setup

1. Flash the current stable Zynthian image (Oram-2511 supports the Pi 5) to the SanDisk card.
2. Webconf → Hardware → Audio: **IQAudio DAC Pro**. A known-good Jack setup from the Zynthian forum for Pi 5 + DAC Pro:
   `-P 70 -s -S -d alsa -d hw:IQaudIODAC -r 48000 -p 128 -n 2 -o 2 -X raw`
3. EEPROM (Pi powered from GPIO 5 V): `sudo -E rpi-eeprom-config --edit`, add the lines from `config/eeprom.conf`, reboot.
4. Enable I²C if Zynthian hasn't (`config/config.txt.snippet`).
5. Battery monitor:
   ```bash
   sudo mkdir -p /opt/electric-sax
   sudo cp battery-monitor/battery_monitor.py /opt/electric-sax/
   sudo pip install smbus2 --break-system-packages
   python3 /opt/electric-sax/battery_monitor.py --once      # sanity check
   sudo cp battery-monitor/battery-monitor.service /etc/systemd/system/
   sudo systemctl enable --now battery-monitor
   journalctl -u battery-monitor -f
   ```
6. H2MIDI: in HxMIDI Tools route USB-A → DIN out **and** USB-A → USB-C, save to the device.

## Power button

The GQ16F button is wired to the Pi 5's J2 pads. Short press: boots when halted, clean shutdown when running (no desktop). Long press: hard off. Only flip the Pi toggle after the Pi has shut down.

## Status

Everything here is written before the hardware arrived and is **untested**. Record test results in `docs/test-log.md`.
