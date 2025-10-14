#!/usr/bin/env python3
import json
import os
import subprocess
import sys

CONFIG_PATH = os.path.expanduser("~/galaxy-notifier/galaxy_config.json")

def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"Configuratiebestand niet gevonden: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    panel_type = config.get("panel_type", "gd").lower()

    if panel_type == "flex":
        script = "GalaxyFlexListener.py"
    else:
        script = "GalaxyListener.py"

    script_path = os.path.join(os.path.expanduser("~/galaxy-notifier"), script)

    if not os.path.exists(script_path):
        print(f"Listener-script niet gevonden: {script_path}")
        sys.exit(1)

    # Vervang het huidige proces met het juiste script
    os.execv(sys.executable, [sys.executable, script_path])

if __name__ == "__main__":
    main()
