# gateway/ws_server.py
import asyncio
import websockets
import json
import paho.mqtt.client as mqtt
import time  # Importa el módulo time
import os  # Importa el módulo os

MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "health/data"

mqtt_client = mqtt.Client()

async def connect_mqtt():
    """Conecta al broker MQTT con reintento."""
    while True:
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print(f"Conectado al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}")
            return  # Sale del bucle si la conexión tiene éxito
        except Exception as e:
            print(f"Error al conectar al broker MQTT: {e}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)

async def handler(websocket):
    from datetime import datetime
    async for message in websocket:
        payload = json.loads(message)
        # Asegura que venga el id y las métricas
        data = {
            "sensor_id":  payload.get("id"),
            "temperature":  payload["temperature"],
            "heart_rate": payload["heart_rate"],
            "blood_pressure": payload["blood_pressure"]
        }
        print("WebSocket recibido:", data)
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))

async def run_ws():
    await connect_mqtt()  # Espera la conexión MQTT
    print("Servidor WebSocket iniciado en el puerto 5002")
    async with websockets.serve(handler, "0.0.0.0", 5002):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(run_ws())