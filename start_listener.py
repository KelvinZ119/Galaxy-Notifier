#!/usr/bin/env python3
import json
import os
import subprocess

CONFIG_PATH = os.path.expanduser("~/Galaxy-Notifier/galaxy_config.json")

if not os.path.exists(CONFIG_PATH):
    print(f"Configuratiebestand niet gevonden: {CONFIG_PATH}")
    exit(1)

with open(CONFIG_PATH) as f:
    cfg = json.load(f)

listener = "GalaxyListener.py" if cfg.get("system_type", "").upper() == "GD" else "GalaxyFlexListener.py"

print(f"Start {listener}...")
subprocess.run(["python3", os.path.join(os.path.dirname(__file__), listener)])
