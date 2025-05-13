FROM python:3.10-slim

WORKDIR /usr/src/app

# Copia e instala dependencias Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código Python
COPY subscriber.py ./

# Variables de entorno por defecto (puedes sobrescribirlas en docker-compose.yml)
ENV PG_HOST=postgres-db \
    PG_PORT=5432 \
    PG_DATABASE=healthdata \
    PG_USER=iotuser \
    PG_PASS=iotpassword \
    MQTT_BROKER=mqtt \
    MQTT_PORT=1883 \
    MQTT_TOPIC=health/data

CMD ["python", "subscriber.py"]
