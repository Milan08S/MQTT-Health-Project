# sensors/websocket_sensor.py
import os
import time
import random
import json
import websocket  # librería cliente WebSocket

# URL del gateway WebSocket
GATEWAY_WS_URL = "ws://gateway:5002/ws"

def generate_health_data():
    """
    Genera un dict con:
      - id tomado de la variable de entorno SENSOR_ID (o 'WS_SENSOR')
      - temperature, heart_rate, blood_pressure
    """
    sensor_id = os.getenv("SENSOR_ID", "WS_SENSOR")
    return {
        "id": sensor_id,
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

def send_data(ws):
    while True:
        data = generate_health_data()
        msg = json.dumps(data)
        ws.send(msg)
        print(f"Enviado: {msg}")
        time.sleep(5)

if __name__ == "__main__":
    # Leer SENSOR_ID opcionalmente de env para distinguir instancias
    ws = websocket.WebSocket()
    try:
        ws.connect(GATEWAY_WS_URL)
        send_data(ws)
    except Exception as e:
        print("Error de conexión:", e)
