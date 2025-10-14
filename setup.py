#!/usr/bin/env python3
import json, os
from rich.prompt import Prompt

CONFIG_PATH = os.path.expanduser("~/Galaxy-Notifier/galaxy_config.json")

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)
    print("\n✅ Configuratie opgeslagen.")

def main():
    print("\nKies het systeemtype:")
    print("1) Galaxy Dimension (RS232/SIA)")
    print("2) Galaxy Flex (USB/Microtech)")
    type_choice = Prompt.ask("Voer je keuze in (1 of 2)", choices=["1", "2"])

    config = {
        "system_type": "GD" if type_choice == "1" else "FLEX",
        "serial_port": Prompt.ask("Seriële poort", default="/dev/ttyUSB0" if type_choice == "1" else "/dev/ttyACM0"),
        "bot_token": Prompt.ask("Telegram bot token"),
        "chat_ids": [int(cid.strip()) for cid in Prompt.ask("Telegram chat ID(s), komma-gescheiden").split(",")]
    }

    if type_choice == "1":
        config.update({
            "baudrate": 9600,
            "databits": 8,
            "parity": "None",
            "stopbits": 1
        })

    save_config(config)

if __name__ == "__main__":
    main()
