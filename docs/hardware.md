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
