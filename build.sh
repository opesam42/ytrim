# build.sh
echo "Starting build script"

pip install -r requirements.txt

# collectstatic
python3 manage.py collectstatic

echo "Build script completed"