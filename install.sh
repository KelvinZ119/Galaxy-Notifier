#!/bin/bash
set -e

echo "Starte installatie Galaxy Notifier..."

# Update & vereiste pakketten
sudo apt update
sudo apt install -y python3 python3-pip python3-serial

# Map voor het project
PROJECT_DIR="$HOME/galaxy-notifier"
mkdir -p "$PROJECT_DIR"

# Kopieer alle bestanden
cp setup.py "$PROJECT_DIR/"
cp GalaxyListener.py "$PROJECT_DIR/"
cp config_template.json "$PROJECT_DIR/galaxy_config.json"
cp -r systemd "$PROJECT_DIR/systemd"

# Installeer Python dependencies
pip3 install --break-system-packages -r requirements.txt

# Maak systemd servicebestand
sudo cp systemd/galaxy-listener.service /etc/systemd/system/galaxy-listener.service

# Pas ExecStart pad aan in service naar jouw projectmap
sudo sed -i "s|/home/pi/GalaxyListener.py|$HOME/galaxy-notifier/GalaxyListener.py|g" /etc/systemd/system/galaxy-listener.service

# Herlaad en start service
sudo systemctl daemon-reload
sudo systemctl enable galaxy-listener.service
sudo systemctl restart galaxy-listener.service

echo "Installatie voltooid. Run 'python3 ~/galaxy-notifier/setup.py' om te configureren."
