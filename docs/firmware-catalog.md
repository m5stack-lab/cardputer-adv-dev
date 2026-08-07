# Third-party firmware tried on this device

Binaries themselves are not committed (see `firmware/downloads/` in
`.gitignore`) — just the provenance and how to refetch them.

## M5Launcher (bmorcelli/Launcher)

- Source: https://github.com/bmorcelli/Launcher
- This is the same project M5Burner lists as "M5Launcher Cardputer & ADV" —
  the repo's release workflow publishes directly to M5Burner
  (`support_files/m5burner_post.py`).
- One binary, `Launcher-m5stack-cardputer.bin`, covers both the original
  Cardputer and the ADV. ADV support is a runtime auto-detect: it probes
  for the TCA8418 I2C keyboard controller and falls back to the original
  GPIO matrix if not found (`boards/m5stack-cardputer/interface.cpp`,
  `UseTCA8418` flag). No separate ADV build exists.
- Flashed version 2.8.0, 2026-08-06. Confirmed boots cleanly on this
  Cardputer ADV, no reboot loop, TCA8418 detected at I2C `0x34` as
  expected.

Fetch:

    gh release download 2.8.0 --repo bmorcelli/Launcher \
      --pattern "Launcher-m5stack-cardputer.bin" \
      --dir firmware/downloads --clobber

Flash (merged image, single write at offset 0x0 — bootloader + partition
table + app all in one file, per `support_files/merge.py` in that repo):

    tools/venv/bin/esptool.py -p /dev/cu.usbmodemXXXX -b 460800 \
      write_flash 0x0 firmware/downloads/Launcher-m5stack-cardputer.bin

### I2C bus scan on this device (from Launcher boot log)

Useful reference for future firmware work — devices found on the ADV's
I2C bus (SDA=8, SCL=9):

| Address | Likely device |
|---------|---------------|
| 0x18    | IMU (BMI270)  |
| 0x34    | TCA8418 keyboard controller |
| 0x43    | Possibly ES8311 audio codec |
| 0x69    | Unidentified — worth investigating |

## Reverting

The flash before this (the `firmware/hello-world` build) is backed up at
`backups/hello-world-baseline.bin`. Restore with:

    tools/venv/bin/esptool.py -p /dev/cu.usbmodemXXXX write_flash 0x0 \
      backups/hello-world-baseline.bin
