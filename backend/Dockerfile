# Imagen base ligera
FROM python:3.12-slim

# Configuración básica
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala las dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto
COPY . .

# Copia el entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Crea usuario sin privilegios
RUN useradd -m appuser
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "blogproj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
