#!/usr/bin/env python3
import json
import os

CONFIG_FILE = os.path.expanduser("~/galaxy-notifier/galaxy_config.json")

def prompt(prompt_text, default=None):
    if default:
        return input(f"{prompt_text} [{default}]: ") or default
    else:
        return input(f"{prompt_text}: ")

def main():
    config = {}
    print("=== Galaxy Notifier Setup ===")

    config["serial_port"] = prompt("Seriële poort (bijv. /dev/ttyUSB0)", "/dev/ttyUSB0")
    config["baudrate"] = int(prompt("Baudrate", "9600"))
    config["databits"] = int(prompt("Databits", "8"))
    config["stopbits"] = int(prompt("Stopbits", "1"))
    config["parity"] = prompt("Pariteit (None, Even, Odd)", "None")
    config["bot_token"] = prompt("Telegram Bot Token", "")
    config["chat_ids"] = prompt("Chat ID's (komma-gescheiden)", "")

    # Schrijf config
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print("Configuratie opgeslagen in", CONFIG_FILE)
    print("Start nu de listener met systemd of handmatig.")

if __name__ == "__main__":
    main()
