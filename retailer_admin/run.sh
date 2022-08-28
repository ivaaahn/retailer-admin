#!/bin/sh

echo "<<< MIGRATIONS >>>"
python manage.py migrate --database=migrations

echo "<<< CREATING SUPERUSER >>>"
python manage.py createsuperuser --noinput --database=migrations

echo "<<< STARTING >>>"
uvicorn retailer_admin.asgi:application "--proxy-headers" --host '0.0.0.0' --port '8000'
