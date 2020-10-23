#! /usr/bin/env bash

# Run custom Python script before starting
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
docker-compose build
docker-compose up -d