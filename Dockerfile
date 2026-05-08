# Usamos una imagen de Python oficial y ligera
FROM python:3.8-slim

# Evita que Python escriba archivos .pyc y fuerza a que el output de consola se vea en los logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalamos abcmidi (¡el paquete crítico del sistema!)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends abcmidi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero el archivo de requerimientos (aprovecha la caché de Docker)
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Exponemos el puerto que usará FastAPI
EXPOSE 8000

# Comando para arrancar el servidor en producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]