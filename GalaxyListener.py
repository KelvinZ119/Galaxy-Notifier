#!/usr/bin/env python3
import serial
import requests
import re
import json
import os
import time

CONFIG_FILE = os.path.expanduser("~/Galaxy-Notifier/galaxy_config.json")
if not os.path.exists(CONFIG_FILE):
    print("Configuratie niet gevonden! Run setup.py eerst.")
    exit(1)

with open(CONFIG_FILE) as f:
    cfg = json.load(f)

BOT_TOKEN = cfg["bot_token"]
CHAT_IDS = cfg["chat_ids"]

ser = serial.Serial(
    cfg["serial_port"],
    baudrate=cfg["baudrate"],
    bytesize={7: serial.SEVENBITS, 8: serial.EIGHTBITS}[cfg["databits"]],
    parity={"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD}[cfg["parity"]],
    stopbits={1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}[cfg["stopbits"]],
    timeout=1
)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message})
        except Exception as e:
            print(f"Telegram-fout voor {chat_id}:", e)

last_sent = ""
waiting = False
event_time = ""

print("Galaxy RS232 listener actief...")

while True:
    try:
        data = ser.readline()
        if not data:
            continue

        msg = data.decode(errors="ignore").strip()
        print("[SIA-Input]", msg)
        ser.write(b'\x06')

        sia_match = re.match(r'^(Oti|Nti|TR|LT|YT)(\d{2}:\d{2})', msg)
        if sia_match:
            event_time = sia_match.group(2)
            waiting = True
            continue

        if waiting and msg.startswith("A"):
            description = re.sub(r"^A[\+\-]?\s*", "", msg).strip()
            final_msg = f"🚨 Galaxy melding om {event_time}:\n📋 {description}"
            if final_msg != last_sent:
                send_to_telegram(final_msg)
                last_sent = final_msg
            waiting = False
            event_time = ""

    except Exception as e:
        print("Fout:", e)
        time.sleep(1)
