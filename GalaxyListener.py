#!/usr/bin/env python3
import serial
import requests
import re
import json
import os
import time

CONFIG_FILE = os.path.expanduser("~/galaxy-notifier/galaxy_config.json")
if not os.path.exists(CONFIG_FILE):
    print("Configuratie niet gevonden! Run setup.py eerst.")
    exit(1)

with open(CONFIG_FILE) as f:
    cfg = json.load(f)

# Telegram instellingen
BOT_TOKEN = cfg["bot_token"]
chat_ids_raw = cfg["chat_ids"]
CHAT_IDS = [int(cid) for cid in chat_ids_raw]

ser = serial.Serial(
    cfg["serial_port"],
    baudrate=cfg["baudrate"],
    bytesize={7: serial.SEVENBITS, 8: serial.EIGHTBITS}[cfg["databits"]],
    parity={ "None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD }[cfg["parity"]],
    stopbits={1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}[cfg["stopbits"]],
    timeout=1
)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        data = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            resp = requests.post(url, data=data)
            if resp.status_code != 200:
                print(f"Telegram-fout voor {chat_id}:", resp.text)
        except Exception as e:
            print(f"Telegram error voor {chat_id}:", e)

last_sent = ""
waiting_for_description = False
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
            waiting_for_description = True
            continue

        if waiting_for_description and msg.startswith("A"):
            description = re.sub(r"^A[\+\-]?\s*", "", msg).strip()
            final_msg = f"🚨 Galaxy melding om {event_time}:\n📋 {description}"

            if final_msg != last_sent:
                send_to_telegram(final_msg)
                last_sent = final_msg
            else:
                print("🔁 Dubbele melding onderdrukt")

            waiting_for_description = False
            event_time = ""

    except Exception as e:
        print("Fout:", e)
        time.sleep(1)
