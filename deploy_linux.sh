#!/bin/bash
set -e

echo "=================================================="
echo "    Atualização de Segurança - Portal Mulher MT   "
echo "=================================================="

# Ir para a raiz do repositório
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

# 1. Puxar as últimas correções do Git
echo "[1/5] Atualizando código-fonte via Git..."
git pull origin main

# 2. Navegar para a pasta do Django e ativar venv
cd "$REPO_DIR/django_portal_mulher"

if [ -d ".venv" ]; then
    echo "[2/5] Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "[2/5] Ativando ambiente virtual (venv)..."
    source venv/bin/activate
else
    echo "[2/5] Usando Python do ambiente ativo..."
fi

# 3. Instalar/atualizar dependências
echo "[3/5] Verificando dependências Python..."
if [ -d "linux_packages" ]; then
    pip install --no-index --find-links=linux_packages/ -r requirements.txt gunicorn 2>/dev/null || pip install -r requirements.txt
else
    pip install -r requirements.txt
fi

# 4. Coleta de estáticos
echo "[4/5] Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || true

# 5. Reiniciar serviço no Linux
echo "[5/5] Reiniciando serviço da aplicação..."
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet portal_mulher 2>/dev/null; then
        sudo systemctl restart portal_mulher
        echo "Serviço 'portal_mulher' reiniciado com sucesso!"
    elif systemctl is-active --quiet gunicorn 2>/dev/null; then
        sudo systemctl restart gunicorn
        echo "Serviço 'gunicorn' reiniciado com sucesso!"
    elif systemctl is-active --quiet portal 2>/dev/null; then
        sudo systemctl restart portal
        echo "Serviço 'portal' reiniciado com sucesso!"
    else
        echo "Aviso: Verifique o nome do serviço systemd configurado (ex: sudo systemctl restart <nome_do_servico>)."
    fi
else
    echo "Aviso: systemctl não disponível neste shell. Reinicie o processo Gunicorn correspondente."
fi

echo "=================================================="
echo "   Atualização concluída com sucesso!             "
echo "=================================================="
