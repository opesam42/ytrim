# Use an official Python image as a base
FROM python:3.10-slim

# Install Chrome and other dependencies
RUN apt-get update && apt-get install -y \
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
  libx11-xcb1 \
  && rm -rf /var/lib/apt/lists/*

# Add Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    dpkg -i google-chrome.deb || apt-get -f install -y && \
    rm google-chrome.deb

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app's code
COPY . /app/

# Command to run your app
CMD ["python", "your_script.py"]
