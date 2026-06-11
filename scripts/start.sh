#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

python manage.py migrate --no-input
python manage.py seed_demo_data --days "${SEED_DAYS:-30}"
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --access-logfile -

