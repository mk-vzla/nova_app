#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt
pip install pymysql
pip install cryptography

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate