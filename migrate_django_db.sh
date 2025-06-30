#!/bin/sh

sleep 5

echo "Migrating Django database."

python ./DjangoDadJokes/manage.py migrate

echo "Django database migration complete."

exec "$@"