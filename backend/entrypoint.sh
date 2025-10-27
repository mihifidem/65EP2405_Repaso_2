#!/usr/bin/env bash
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recogiendo archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."
exec "$@"
