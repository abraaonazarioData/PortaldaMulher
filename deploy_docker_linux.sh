#!/bin/bash
set -e

# ==============================================================================
# Script de Deploy e Inicialização com Docker — Portal Mulher MT (Linux)
# ==============================================================================

echo "=========================================================="
echo "    Iniciando Deploy Seguro no Linux - Portal Mulher MT   "
echo "=========================================================="

# 1. Garantir que estamos no diretório do projeto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 2. Verificar se o Docker e Docker Compose estão instalados
if ! command -v docker &> /dev/null; then
    echo "ERRO: O Docker não está instalado neste servidor Linux."
    echo "Instale o Docker antes de continuar: https://docs.docker.com/engine/install/"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "ERRO: O Docker Compose (plugin) não está disponível."
    echo "Instale o plugin docker-compose-plugin."
    exit 1
fi

# 3. Verificar arquivo de configuração de variáveis de ambiente
if [ ! -f ".env.docker" ]; then
    if [ -f ".env.docker.example" ]; then
        echo "Aviso: .env.docker não encontrado. Criando cópia a partir de .env.docker.example..."
        cp .env.docker.example .env.docker
        echo "IMPORTANTE: Revise o arquivo .env.docker com os dados de produção!"
    else
        echo "ERRO: Arquivo .env.docker não encontrado!"
        exit 1
    fi
fi

# 4. Construir e iniciar os contêineres em segundo plano
echo "[1/3] Construindo imagem Docker atualizada..."
docker compose build

echo "[2/3] Iniciando serviços via Docker Compose..."
docker compose up -d

# 5. Aguardar e verificar o status de saúde
echo "[3/3] Verificando integridade da aplicação..."
sleep 5

if docker compose ps | grep -q "portal_mulher_app"; then
    echo "=========================================================="
    echo "  Deploy concluído com sucesso no servidor Linux!         "
    echo "  Status do contêiner:                                    "
    docker compose ps
    echo "=========================================================="
    echo "Comandos úteis:"
    echo "  - Ver logs em tempo real: docker compose logs -f"
    echo "  - Parar o serviço:        docker compose down"
    echo "  - Reiniciar o serviço:    docker compose restart"
    echo "=========================================================="
else
    echo "ERRO: O contêiner não iniciou corretamente. Verifique os logs com: docker compose logs"
    exit 1
fi
