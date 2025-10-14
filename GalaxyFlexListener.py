# Galaxy Flex USB Listener (Microtech Protocol)
# Kelvin-config compatible

import serial
import json
import time
import os
import sys
import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / "galaxy-notifier" / "config.json"

def load_config():
    if not CONFIG_PATH.exists():
        print("[!] Config bestand niet gevonden. Draai eerst setup.py.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def main():
    config = load_config()

    if config.get("protocol") != "flex":
        print("[!] Deze listener is alleen bedoeld voor Flex (Microtech USB). Protocol in config.json moet 'flex' zijn.")
        sys.exit(1)

    port = config.get("serial_port", "/dev/ttyACM0")
    baudrate = int(config.get("baudrate", 9600))

    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        log(f"Luistert op {port} @ {baudrate} baud...")
    except serial.SerialException as e:
        log(f"Fout bij openen van seriele poort: {e}")
        sys.exit(1)

    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                log(f"Flex: {line}")
                # Hier kun je parsing toevoegen als je weet welk formaat het is
                # Bijvoorbeeld split op komma’s als het ASCII is: evt,zone,user,etc.

            time.sleep(0.1)
    except KeyboardInterrupt:
        log("Afsluiten...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
