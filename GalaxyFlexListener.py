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

ser = serial.Serial(cfg["serial_port"], baudrate=9600, timeout=1)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message})
        except Exception as e:
            print(f"Telegram-fout voor {chat_id}:", e)

print("Galaxy Flex listener actief...")

while True:
    try:
        data = ser.readline()
        if not data:
            continue

        msg = data.decode(errors="ignore").strip()
        print("[Flex Input]", msg)
        send_to_telegram(f"📡 Flex: {msg}")

    except Exception as e:
        print("Fout:", e)
        time.sleep(1)
