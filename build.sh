#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Recolectar estáticos (CSS/JS) en la carpeta staticfiles
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos de producción
python manage.py migrate