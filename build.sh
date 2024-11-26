#!/bin/bash

# Install Google Chrome
echo "Installing Google Chrome..."

# Add Google's signing key and the repository to install Chrome
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb
dpkg -i google-chrome.deb
apt-get -f install -y

# Install dependencies for running Selenium and Chrome headless
apt-get update
apt-get install -y \
  wget \
  curl \
  gnupg2 \
  ca-certificates \
  unzip \
  libnss3 \
  libgdk-pixbuf2.0-0 \
  libxss1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libxcomposite1 \
  libxrandr2 \
  libgbm1 \
  libpango-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libx11-xcb1

# Clean up
rm google-chrome.deb

echo "Google Chrome installed successfully"