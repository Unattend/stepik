#!/bin/bash
python manage.py migrate
gunicorn -b :8000 stepik.wsgi --access-logfile - --error-logfile -
