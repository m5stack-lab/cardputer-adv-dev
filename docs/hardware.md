# M5Stack Cardputer ADV — Hardware Notes

## Confirmed specs (from M5Stack shop listing, CNX Software, Botland)

- Core module: M5Stamp-S3A, built on ESP32-S3FN8
  - Dual-core Xtensa LX7, up to 240 MHz
  - 8 MB Flash, **no PSRAM** (per `FN8` module suffix — no `R` = no PSRAM)
  - Note: some secondary sources report 4MB flash / 8MB PSRAM — those look
    wrong/confused with other Cardputer variants. Treat as unconfirmed until
    we read it back from the chip directly (see below).
- Display: 1.14" LCD
- Input: 56-key keyboard
- Audio (new on ADV vs. original Cardputer): ES8311 codec, MEMS mic, NS4150B
  amp, 1W speaker, 3.5mm headphone jack
- IMU: BMI270 6-axis (new on ADV)
- Battery: 1750 mAh (larger than original Cardputer)
- USB: native USB-CDC on the S3 (no external USB-serial chip expected, but
  confirm port name when connected — see tools/device.py)

## Source of truth

Don't trust any of the above blindly for flash-size-sensitive config
(partition tables, OTA layout). Once the device is connected, run:

    tools/venv/bin/python tools/device.py info

This reads actual chip/flash/MAC info directly off the device via esptool
and is authoritative over anything written here.

Confirmed via UIFlow2 (uiflow2.m5stack.com, WebSerial): Controller reports
as `Cardputer-Adv`, SoC `ESP32-S3`, matching the assumptions above.

Confirmed via esptool during first flash (2026-08-06):

    Chip is ESP32-S3 (QFN56) (revision v0.2)
    Features: WiFi, BLE, Embedded Flash 8MB (GD)
    Crystal is 40MHz
    USB mode: USB-Serial/JTAG
    MAC: 80:45:6b:76:fa:68

8MB flash confirmed. No PSRAM listed under Features, matching the `FN8`
(no-PSRAM) assumption — treat as confirmed now.

## USB connection gotcha (learned 2026-08-06)

The bundled/included USB-C cable was **charge-only** (no data lines) — the
device drew power and its screen worked fine, but macOS never enumerated
any new serial device (`ls /dev/cu.*`, `system_profiler`, and Chrome's
native WebSerial picker all showed nothing). Confirmed by testing with a
known-data-capable cable, after which the device immediately appeared as
`/dev/cu.usbmodemXXXX`. If the device seems "invisible" over USB, try a
different cable before suspecting drivers/firmware/OS config.

Also: only one process can own the serial port at a time. If `esptool`
reports `Resource busy`, check for another connection first
(`lsof /dev/cu.usbmodemXXXX`) — commonly a browser tab with UIFlow2 or a
`pio device monitor` session left open.

## PlatformIO board choice

PlatformIO's `espressif32` platform has no dedicated `cardputer` board
entry. The standard approach (used by M5Stack's own examples and the
community) is to build on the generic `esp32-s3-devkitc-1` board and
override flash size / PSRAM / USB flags manually. See
`firmware/hello-world/platformio.ini`.

## Sources

- https://shop.m5stack.com/products/m5stack-cardputer-adv-version-esp32-s3
- https://www.cnx-software.com/2025/10/23/m5stack-cardputer-adv-esp32-s3-computer-gains-improved-antenna-larger-1750-mah-battery-es8311-audio-codec/
- https://botland.store/stamp-series/27278-m5stack-cardputer-adv-version-portable-computer-with-m5stamp-s3a-module-esp32-s3fn8-m5stack-k132-adv-6972934176097.html
