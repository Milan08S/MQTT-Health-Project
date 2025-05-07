import time
import random
import json
import websocket  # Esta librería es diferente de "websockets" (de asyncio)

GATEWAY_WS_URL = "ws://gateway:5002/ws"  # Cambia el puerto si es diferente

def generate_health_data():
    return {
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "heart_rate": random.randint(60, 100),
        "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

def send_data(ws):
    while True:
        data = json.dumps(generate_health_data())
        ws.send(data)
        print(f"Enviado: {data}")
        time.sleep(5)

if __name__ == "__main__":
    ws = websocket.WebSocket()
    try:
        ws.connect(GATEWAY_WS_URL)
        send_data(ws)
    except Exception as e:
        print("Error de conexión:", e)
