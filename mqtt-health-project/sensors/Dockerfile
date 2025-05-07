# Dockerfile para sensor REST con imagen segura
FROM python:3.13-slim

# Actualizar el sistema base
RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY . /app

# Instala solo las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "rest_sensor.py"]
