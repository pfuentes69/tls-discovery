#!/bin/bash

set -e

echo "[*] Installing required tools (Docker, zmap, Python3)..."

# Update and install system packages
sudo apt update
sudo apt install -y zmap python3 python3-pip docker.io

echo "[*] Enabling and starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[*] Pulling zgrab2 Docker image..."
docker pull ghcr.io/zmap/zgrab2

echo "[+] Setup complete. You're ready to run the pipeline!"
