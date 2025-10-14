
import json
import os

CONFIG_PATH = os.path.expanduser("~/galaxy-notifier/config.json")
CONFIG_TEMPLATE_PATH = os.path.expanduser("~/Galaxy-Notifier/config_template.json")

def load_config_template():
    with open(CONFIG_TEMPLATE_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("\nConfiguratie opgeslagen in", CONFIG_PATH)

def get_input(prompt, default=None):
    value = input(f"{prompt} [{'Enter' if default else ''}] ") or default
    return value

def main():
    print("Galaxy Notifier configuratie starten...\n")

    config = load_config_template()

    # Keuze tussen GD en Flex
    print("Kies het systeemtype:")
    print("1) Galaxy Dimension (RS232/SIA)")
    print("2) Galaxy Flex (USB/Microtech)")
    choice = input("Voer je keuze in (1 of 2): ").strip()

    if choice == "2":
        config["protocol"] = "flex"
        config["serial_port"] = get_input("Seriële poort (bijv. /dev/ttyACM0)", "/dev/ttyACM0")
        config["baudrate"] = 9600  # fixed for Flex
        config["bytesize"] = 8
        config["parity"] = "N"
        config["stopbits"] = 1
    else:
        config["protocol"] = "gd"
        config["serial_port"] = get_input("Seriële poort (bijv. /dev/ttyUSB0)", "/dev/ttyUSB0")
        config["baudrate"] = int(get_input("Baudrate", "9600"))
        config["bytesize"] = int(get_input("Byte size", "8"))
        config["parity"] = get_input("Parity (N/E/O)", "N")
        config["stopbits"] = int(get_input("Stop bits", "1"))

    config["telegram_bot_token"] = get_input("Telegram bot token", config.get("telegram_bot_token", ""))
    config["telegram_chat_id"] = get_input("Telegram chat ID", config.get("telegram_chat_id", ""))

    save_config(config)
    print("\nStart nu de listener met systemd of handmatig.")

if __name__ == "__main__":
    main()
