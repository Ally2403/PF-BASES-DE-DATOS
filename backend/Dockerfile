FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para oracledb
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (capa cacheada)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente (será sobreescrito por el volumen en desarrollo)
COPY . .

# Exponer el puerto de la API
EXPOSE 8000

# Arrancar con --reload para que detecte cambios en el volumen
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
