# ============================================================================
# Dockerfile — Portal Mulher MT (Produção e Hardening de Segurança)
# Compatível com Windows (Docker Desktop) e Linux (Docker Engine / Swarm / K8s)
# ============================================================================

FROM python:3.12-slim-bookworm

# 1. Metadados e variáveis de ambiente seguras para Python
LABEL maintainer="Portal Mulher MT" \
      description="Ambiente conteinerizado seguro do Portal Mulher MT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000

# 2. Instalar dependências essenciais do sistema operacional e utilitário de saúde (curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Criação de usuário e grupo de sistema exclusivo sem privilégios de root (Hardening)
RUN groupadd -r -g 10001 portalgroup && \
    useradd -r -u 10001 -g portalgroup -d /app -s /sbin/nologin portaluser

# 4. Definir diretório de trabalho da aplicação
WORKDIR /app

# 5. Instalar dependências Python primeiro (aproveitamento eficiente do cache do Docker)
COPY django_portal_mulher/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiar o script de entrypoint e assegurar formato de linha POSIX (LF) para evitar erro no Windows
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# 7. Copiar o código-fonte da aplicação Django
COPY django_portal_mulher/ /app/

# 8. Criar diretórios de persistência e ajustar posse e permissões estritas para portaluser
RUN mkdir -p /app/media /app/staticfiles /app/data && \
    chown -R portaluser:portalgroup /app && \
    chmod -R 755 /app

# 9. Trocar para o usuário restrito não-root (Princípio do Menor Privilégio)
USER portaluser

# 10. Expor a porta da aplicação
EXPOSE 8000

# 11. Healthcheck automático de disponibilidade
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 12. Ponto de entrada e comando de execução padrão em produção
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "portal_django.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "4", "--worker-class", "gthread", "--timeout", "120", "--keep-alive", "5"]
