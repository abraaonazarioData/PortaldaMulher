#!/bin/bash
# Script rápido para iniciar o Portal Mulher MT manualmente no Linux
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR/django_portal_mulher"

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

export DJANGO_DEBUG=False
export DJANGO_PRODUCTION=True
export DJANGO_ALLOWED_HOSTS="*,192.168.171.79,localhost,127.0.0.1,mulher.mt.gov.br"
export CSRF_TRUSTED_ORIGINS="http://192.168.171.79,http://192.168.171.79:80,http://localhost:80,https://mulher.mt.gov.br"

echo "=========================================================="
echo "   Iniciando Portal Mulher MT na porta 80..."
echo "=========================================================="

# Se a porta 80 exigir privilégio de root no terminal manual:
if command -v gunicorn &>/dev/null; then
    gunicorn portal_django.wsgi:application --bind 0.0.0.0:80 --workers 3 --threads 4 --timeout 120
else
    python3 manage.py runserver 0.0.0.0:80
fi
