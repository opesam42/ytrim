#!/bin/bash
echo "Starting build script"

python3 -m venv venv
source venv/bin/activate

echo "setup virtural env"

# Use Python 3 to ensure pip is found
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# collectstatic
python3 manage.py collectstatic --noinput

#deactivate virural environment
deactivate

echo "Build script completed"