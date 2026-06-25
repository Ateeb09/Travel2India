#!/usr/bin/env bash
# exit on error
set -o errexit

# If running from repository root, move into travel2india directory
if [ -d "travel2india" ]; then
    cd travel2india
fi

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
