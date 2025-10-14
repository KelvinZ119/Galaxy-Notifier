#!/bin/bash
echo "Starte installatie Galaxy Notifier..."

sudo apt update
sudo apt install -y python3 python3-pip python3-serial

pip3 install --user -r requirements.txt

# Systeemdienst installeren
sudo cp systemd/galaxy-listener.service /etc/systemd/system/galaxy-listener.service
sudo systemctl daemon-reload
sudo systemctl enable galaxy-listener.service

# Config template kopiëren
cp config_template.json galaxy_config.json

echo "Installatie voltooid. Start nu: python3 setup.py"
