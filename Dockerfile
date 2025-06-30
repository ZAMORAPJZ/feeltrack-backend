# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el contenido del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 (FastAPI por defecto)
EXPOSE 8000

# Comando para iniciar la app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]