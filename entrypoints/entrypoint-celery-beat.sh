#! /bin/bash -eu

celery --app=main.celeryconf beat \
  --loglevel=INFO \
  --schedule=/var/run/celery/celerybeat-schedule
