#!/usr/bin/env bash
# Exit on error
set -o errexit

# Step 1: Install system dependencies
echo "Installing system dependencies and Google Chrome..."

# Download the Google Chrome .deb package
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb

# Install the Chrome .deb package and fix any missing dependencies
apt-get update
apt-get install -y ./google-chrome.deb || apt-get -f install -y

# Install additional dependencies for running Selenium and Chrome headless
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

# Clean up to save space
rm google-chrome.deb
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "System dependencies installed successfully."

# Step 2: Install Python dependencies
echo "Installing Python dependencies..."

# Ensure `pip` is up-to-date
pip install --upgrade pip

# Install requirements from `requirements.txt`
pip install -r requirements.txt

echo "Python dependencies installed successfully."
