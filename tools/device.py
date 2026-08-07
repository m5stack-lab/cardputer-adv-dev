#!/usr/bin/env python3
"""Talk to the M5Stack Cardputer ADV over USB.

Thin wrapper around esptool/pyserial for the workflows this project needs:
detecting the device, reading back real chip/flash info, opening a serial
monitor, and dumping a full flash backup before trying new firmware.

Usage:
    device.py ports                 list candidate serial ports
    device.py info [PORT]           print chip/flash/MAC info (source of truth)
    device.py monitor [PORT] [BAUD] open a serial monitor (default 115200)
    device.py backup [PORT] [OUT]   dump the full flash to backups/ (or OUT)
"""
import glob
import subprocess
import sys
import time
from pathlib import Path

VENV_BIN = Path(__file__).resolve().parent / "venv" / "bin"
ESPTOOL = str(VENV_BIN / "esptool.py")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = PROJECT_ROOT / "backups"

CANDIDATE_GLOBS = [
    "/dev/cu.usbmodem*",
    "/dev/cu.usbserial*",
    "/dev/cu.wchusbserial*",
    "/dev/cu.SLAB_USBtoUART*",
    "/dev/cu.CH9102*",
]


def find_ports():
    ports = []
    for pattern in CANDIDATE_GLOBS:
        ports.extend(glob.glob(pattern))
    return sorted(set(ports))


def pick_port(explicit):
    if explicit:
        return explicit
    ports = find_ports()
    if not ports:
        sys.exit(
            "No candidate serial device found. Plug the Cardputer ADV in over "
            "USB-C and try again, or check `device.py ports` / System "
            "Information > USB for what shows up."
        )
    if len(ports) > 1:
        print("Multiple candidate ports found, using the first:", ports)
    return ports[0]


def cmd_ports(_args):
    ports = find_ports()
    if not ports:
        print("No candidate serial ports found.")
    for p in ports:
        print(p)


def cmd_info(args):
    port = pick_port(args[0] if args else None)
    print(f"Querying {port} ...")
    subprocess.run([ESPTOOL, "-p", port, "flash_id"], check=True)


def cmd_monitor(args):
    port = pick_port(args[0] if args else None)
    baud = args[1] if len(args) > 1 else "115200"
    print(f"Opening monitor on {port} @ {baud} (Ctrl+] to exit)")
    subprocess.run(
        [str(VENV_BIN / "python"), "-m", "serial.tools.miniterm", port, baud],
        check=True,
    )


def cmd_backup(args):
    port = pick_port(args[0] if args else None)
    out = args[1] if len(args) > 1 else None
    if out is None:
        BACKUPS_DIR.mkdir(exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        out = str(BACKUPS_DIR / f"flash-backup-{stamp}.bin")

    # Read detected flash size off the chip rather than assuming it.
    result = subprocess.run(
        [ESPTOOL, "-p", port, "flash_id"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    size_str = None
    for line in result.stdout.splitlines():
        if "Detected flash size" in line:
            size_str = line.split(":")[-1].strip()
    if not size_str:
        sys.exit("Could not detect flash size from esptool output.")

    units = {"MB": 1024 * 1024, "KB": 1024, "B": 1}
    for suffix, mult in units.items():
        if size_str.upper().endswith(suffix):
            size_bytes = int(float(size_str[: -len(suffix)].strip()) * mult)
            break
    else:
        sys.exit(f"Could not parse flash size {size_str!r} into bytes.")

    print(f"Backing up {size_str} ({size_bytes} bytes) of flash from {port} to {out}")
    subprocess.run(
        [
            ESPTOOL, "-p", port, "-b", "460800",
            "read_flash", "0", str(size_bytes), out,
        ],
        check=True,
    )
    print(f"Done: {out}")


COMMANDS = {
    "ports": cmd_ports,
    "info": cmd_info,
    "monitor": cmd_monitor,
    "backup": cmd_backup,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
