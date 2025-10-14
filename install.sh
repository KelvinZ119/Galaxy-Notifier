#!/bin/bash
set -e

echo "Starte installatie Galaxy Notifier..."

# Update & vereiste pakketten
sudo apt update
sudo apt install -y python3 python3-pip python3-serial

# Pad naar projectmap
PROJECT_DIR="$HOME/Galaxy-Notifier"

# Installeer Python dependencies
pip3 install --break-system-packages -r "$PROJECT_DIR/requirements.txt"

# Zet systemd service
sudo cp "$PROJECT_DIR/systemd/galaxy-listener.service" /etc/systemd/system/galaxy-listener.service

# Pas ExecStart pad aan in service naar jouw projectmap
sudo sed -i "s|/home/pi/GalaxyListener.py|$PROJECT_DIR/GalaxyListener.py|g" /etc/systemd/system/galaxy-listener.service

# Herlaad en start service
sudo systemctl daemon-reload
sudo systemctl enable galaxy-listener.service
sudo systemctl restart galaxy-listener.service
cp "$PROJECT_DIR/config_template.json" "$PROJECT_DIR/config_template.json"


echo "Installatie voltooid. Run 'python3 $PROJECT_DIR/setup.py' om te configureren."
