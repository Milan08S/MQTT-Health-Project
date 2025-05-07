# sensors/rest_sensor.py
import os
import time
import requests
import random
import json

# URL del gateway REST
GATEWAY_URL = "http://gateway:5000/data"

def generate_health_data():
    """
    Genera un dict con:
      - sensor_id tomado de la variable de entorno SENSOR_ID (o 'REST_SENSOR')
      - temperature, heart_rate, blood_pressure
    """
    sensor_id = os.getenv("SENSOR_ID", "REST_SENSOR")
    return {
        "id": sensor_id,
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

def run():
    while True:
        data = generate_health_data()
        try:
            resp = requests.post(GATEWAY_URL, json=data)
            print(f"Enviado: {data} | Respuesta: {resp.status_code}")
        except Exception as e:
            print(f"Error al enviar datos: {e}")
        time.sleep(5)

if __name__ == "__main__":
    run()