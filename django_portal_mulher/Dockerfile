# Imagem base oficial do Python slim (leve e rápida)
FROM python:3.12-slim

# Evita geração de bytecode .pyc e força flush imediato dos logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências de compilação essenciais e utilitários
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . /app/

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput || true

# Porta de execução
EXPOSE 8000

# Executa o Django diretamente em modo de serviço de estáticos
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
