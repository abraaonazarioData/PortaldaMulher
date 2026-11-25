#!/bin/sh
set -e

echo "=== [Portal Mulher MT] Iniciando contêiner seguro ==="

# 1. Garantir que as pastas de mídia, estáticos e dados existam
mkdir -p /app/media /app/staticfiles /app/data

# 2. Inicializar banco de dados persistente caso seja o primeiro boot
if [ -n "$DJANGO_DB_PATH" ]; then
    DB_DIR="$(dirname "$DJANGO_DB_PATH")"
    mkdir -p "$DB_DIR"
    if [ ! -f "$DJANGO_DB_PATH" ] && [ -f "/app/db.sqlite3" ]; then
        echo "-> Inicializando banco de dados persistente a partir do backup populado..."
        cp /app/db.sqlite3 "$DJANGO_DB_PATH"
    fi
fi

# 3. Executar migrações do banco de dados
echo "-> Verificando e aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 4. Coletar e comprimir arquivos estáticos (WhiteNoise)
echo "-> Coletando arquivos estáticos para produção..."
python manage.py collectstatic --noinput

# 5. Executar o comando principal passado para o contêiner (ex: Gunicorn)
echo "-> Iniciando servidor de aplicação..."
exec "$@"
