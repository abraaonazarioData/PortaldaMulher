#!/bin/bash
set -e

echo "=================================================="
echo "    Atualização de Segurança - Portal Mulher MT   "
echo "=================================================="

# Ir para a raiz do repositório
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

# 1. Puxar as últimas correções do Git (se for repositório configurado)
if [ -d ".git" ] && git remote get-url origin &>/dev/null; then
    echo "[1/6] Atualizando código-fonte via Git..."
    git pull origin main || echo "Aviso: git pull não executado, mantendo arquivos locais..."
else
    echo "[1/6] Utilizando arquivos locais descompactados..."
fi

# 2. Navegar para a pasta do Django e ativar venv
cd "$REPO_DIR/django_portal_mulher"

if [ -d ".venv" ]; then
    echo "[2/6] Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "[2/6] Ativando ambiente virtual (venv)..."
    source venv/bin/activate
elif command -v python3 &>/dev/null; then
    echo "[2/6] Criando e ativando novo ambiente virtual Linux (.venv)..."
    python3 -m venv .venv || true
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
else
    echo "[2/6] Usando Python do ambiente ativo..."
fi

# 3. Instalar/atualizar dependências
echo "[3/6] Verificando dependências Python..."
if [ -d "linux_packages" ]; then
    echo "Tentando instalar pacotes offline (linux_packages)..."
    pip install --no-index --find-links=linux_packages/ -r requirements.txt || {
        echo "Aviso: Nem todos os pacotes estavam presentes em linux_packages. Instalando via repositório online..."
        pip install -r requirements.txt
    }
else
    pip install -r requirements.txt
fi

# 4. Migração de banco de dados
echo "[4/6] Aplicando migrações pendentes no banco de dados..."
python manage.py migrate --noinput

# 5. Coleta de arquivos estáticos
echo "[5/6] Coletando arquivos estáticos para produção..."
mkdir -p staticfiles
python manage.py collectstatic --noinput

# 6. Reiniciar serviço no Linux
echo "[6/6] Reiniciando serviço da aplicação..."
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
