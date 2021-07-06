#!/bin/sh

python /code/manage.py collectstatic --no-input
python /code/manage.py migrate --no-input

exec "$@"
