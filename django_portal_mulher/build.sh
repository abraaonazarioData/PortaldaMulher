#!/usr/bin/env bash
# Build script para Render e ambientes PaaS
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
