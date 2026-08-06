# cardputeradv

Development project for the M5Stack Cardputer ADV (ESP32-S3).

## Layout

- `tools/` — local Python venv + scripts for talking to the device
  (detect/info/monitor/backup) via `esptool`. Not committed (see
  `.gitignore`); recreate with `python3 -m venv tools/venv && tools/venv/bin/pip install esptool platformio`.
- `firmware/` — PlatformIO projects. `firmware/hello-world/` is the first
  minimal Arduino + M5Unified sketch, used to validate the build/flash
  pipeline end to end.
- `docs/` — hardware notes and other reference material.

## Quick start

1. Plug the Cardputer ADV in over USB-C.
2. Check the device is detected and read its actual chip/flash info:

   ```
   tools/venv/bin/python tools/device.py info
   ```

3. Build and flash the hello-world firmware:

   ```
   cd firmware/hello-world
   ../../tools/venv/bin/pio run -t upload
   ../../tools/venv/bin/pio device monitor
   ```

See `docs/hardware.md` for hardware specs and sourcing notes.
