#!/bin/sh
set -e

echo "=== [Portal Mulher MT] Iniciando contêiner seguro ==="

# 1. Garantir que as pastas de mídia e estáticos existam
mkdir -p /app/media /app/staticfiles

# 2. Executar migrações do banco de dados
echo "-> Verificando e aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 3. Coletar e comprimir arquivos estáticos (WhiteNoise)
echo "-> Coletando arquivos estáticos para produção..."
python manage.py collectstatic --noinput

# 4. Executar o comando principal passado para o contêiner (ex: Gunicorn)
echo "-> Iniciando servidor de aplicação..."
exec "$@"
