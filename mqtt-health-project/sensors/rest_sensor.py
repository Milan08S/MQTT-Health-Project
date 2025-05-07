# rest_sensor.py
import time
import requests
import random
import json

GATEWAY_URL = "http://gateway:5000/data"  # el gateway escucha en este puerto

def generate_health_data():
    return {
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

while True:
    data = generate_health_data()
    try:
        response = requests.post(GATEWAY_URL, json=data)
        print(f"Enviado: {data} | Respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar datos: {e}")
    time.sleep(5)
