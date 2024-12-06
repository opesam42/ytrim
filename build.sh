#!/bin/bash
echo "Starting build script"

# Use Python 3 to ensure pip is found
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# collectstatic
python3 manage.py collectstatic --noinput

echo "Build script completed"