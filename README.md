# Galaxy Notifier

## Installatie

Op een verse Raspberry Pi OS Lite:

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-serial
cd ~
git clone https://github.com/<jouw-gebruiker>/galaxy-notifier.git
cd galaxy-notifier
chmod +x install.sh
./install.sh
