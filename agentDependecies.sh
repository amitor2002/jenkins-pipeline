#!/bin/bash

set -e

echo "=================================="
echo "🔥 Jenkins Agent SSH Setup Script 🔥"
echo "=================================="

# === updating system ===
echo "🔧 Updating system package index..."
sudo apt-get update -y

# === install dependencies ===
install_if_missing() {
    if ! dpkg -s "$1" &> /dev/null; then
        echo "📦 Installing $1..."
        sudo apt-get install -y "$1"
    else
        echo "✅ $1 already installed."
    fi
}

DEPENDENCIES=(curl ca-certificates lsb-release gnupg git python3 python3-venv python3-pip openjdk-11-jdk openssh-server)

for pkg in "${DEPENDENCIES[@]}"; do
    install_if_missing "$pkg"
done

# === install docker if missing ===
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "✅ Docker already installed."
fi

# === check Java ===
echo "☕ Verifying Java version:"
java -version

# === check SSH ===
echo "🔐 Verifying SSH server status..."
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh --no-pager

echo "✅ Jenkins SSH-based agent setup complete. You can now connect from the controller!"
