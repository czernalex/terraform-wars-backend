#!/bin/bash -eu

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}

gunicorn main.asgi:application --preload --workers=${1:-2} --timeout 0 --worker-class uvicorn_worker.UvicornWorker --bind ${HOST}:${PORT} --log-level=info
