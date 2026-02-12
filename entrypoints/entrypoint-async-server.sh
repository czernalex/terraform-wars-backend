#!/bin/bash -eu

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}

gunicorn main.asgi:application --preload --workers=${1:-2} --timeout 0 --worker-class asgi --worker-connections 1000 --bind ${HOST}:${PORT} --log-level=info
