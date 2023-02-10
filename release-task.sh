#!/bin/sh

python manage.py migrate 

gunicorn WeatherData.wsgi:application --bind 127.0.0.1:8000
