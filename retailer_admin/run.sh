#!/bin/sh

python manage.py migrate --database=migrations
sleep 15
python manage.py createsuperuser --noinput
uvicorn retailer_admin.asgi:application "--proxy-headers" --host '0.0.0.0' --port '8000' --reload
