FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al iniciar el contenedor
CMD ["python", "-u", "producer_gps.py"]
