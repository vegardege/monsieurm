#!/usr/bin/env sh
# Load variables from .env
set -a
[ -f /app/.env ] && . /app/.env
set +a

# Exec the CLI
exec poetry run monsieurm "$@"
