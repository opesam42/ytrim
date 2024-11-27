#!/bin/bash

echo "Starting build script"

# Install the required Python dependencies from requirements.txt
pip install -r requirements.txt

# Install Playwright and the required browsers (Chromium, Webkit, Firefox)
python3 -m pip install playwright
python3 -m playwright install --with-deps chromium

# Make database migrations
python3 manage.py makemigrations

# Apply migrations to the database
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

echo "Build script completed"
