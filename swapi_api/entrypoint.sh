#!/bin/bash

# Wait until database is ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Exec migrations
python manage.py migrate

# Create the superuser using the custom command
python manage.py create_superuser

# Init Gunicorn
exec "$@"
