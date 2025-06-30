FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Usa el puerto dinámico de Render
EXPOSE 8000

# Usa la variable de entorno PORT que Render define
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]