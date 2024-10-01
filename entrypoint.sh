#!/bin/bash

# Espera pelo PostgreSQL estar disponível
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Executa migrações do Django
python manage.py makemigrations
python manage.py migrate

# Coleta arquivos estáticos (se necessário)
python manage.py collectstatic --noinput

# Inicia o servidor Django
exec "$@"
