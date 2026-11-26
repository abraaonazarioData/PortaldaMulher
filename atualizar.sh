#!/bin/bash
# ==============================================================================
# Script de Atualização Rápida no Linux (Atualiza apenas o que já está instalado)
# ==============================================================================

set -e

echo "=========================================================="
echo "   Atualizando o Portal Mulher MT existente...            "
echo "=========================================================="

# 1. Localizar pasta do Django
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/django_portal_mulher/manage.py" ]; then
    APP_DIR="$SCRIPT_DIR/django_portal_mulher"
elif [ -f "$SCRIPT_DIR/manage.py" ]; then
    APP_DIR="$SCRIPT_DIR"
else
    echo "ERRO: manage.py não encontrado em $SCRIPT_DIR!"
    exit 1
fi

cd "$APP_DIR"
echo "Pasta da aplicação: $APP_DIR"

# 2. Ativar o ambiente virtual existente
if [ -f ".venv/bin/activate" ]; then
    echo "-> Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    echo "-> Ativando ambiente virtual (venv)..."
    source venv/bin/activate
elif [ -f "../.venv/bin/activate" ]; then
    echo "-> Ativando ambiente virtual (../.venv)..."
    source ../.venv/bin/activate
else
    echo "Aviso: Ambiente virtual não detectado, usando python3 do sistema..."
fi

# 3. Fazer backup preventivo do banco de dados atual
if [ -f "db.sqlite3" ]; then
    BACKUP_NAME="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    cp db.sqlite3 "$BACKUP_NAME"
    echo "-> Backup do banco salvo como: $BACKUP_NAME"
fi

# 4. Atualizar dependências (se houver novas)
echo "-> Verificando dependências Python..."
pip install -r requirements.txt --quiet

# 5. Aplicar novas migrações
echo "-> Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 6. Atualizar arquivos estáticos (CSS, JS, imagens)
echo "-> Atualizando arquivos estáticos para produção..."
python manage.py collectstatic --noinput

# 7. Reiniciar o serviço em execução
echo "-> Reiniciando serviço do portal..."
if systemctl is-active --quiet portal_mulher 2>/dev/null; then
    sudo systemctl restart portal_mulher
    echo "-> Serviço 'portal_mulher' reiniciado com sucesso!"
elif systemctl is-active --quiet gunicorn 2>/dev/null; then
    sudo systemctl restart gunicorn
    echo "-> Serviço 'gunicorn' reiniciado com sucesso!"
elif systemctl is-active --quiet portal 2>/dev/null; then
    sudo systemctl restart portal
    echo "-> Serviço 'portal' reiniciado com sucesso!"
else
    echo "Aviso: Nenhum serviço com nome 'portal_mulher' ou 'gunicorn' está ativo."
    echo "Se você roda manualmente com Gunicorn, reinicie o processo correspondente."
fi

echo "=========================================================="
echo "   Atualização concluída com sucesso!                     "
echo "=========================================================="
