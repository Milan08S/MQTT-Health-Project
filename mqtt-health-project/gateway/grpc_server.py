# gateway/grpc_server.py

from concurrent import futures
import grpc.aio
import logging
import json
from datetime import datetime
import health_pb2
import health_pb2_grpc
import paho.mqtt.client as mqtt
import time  # Importa el módulo time
import os  # Importa el módulo os
import asyncio # Importa el módulo asyncio

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

class HealthService(health_pb2_grpc.HealthServiceServicer):
    def SendHealthData(self, request, context):
        # Construye el mensaje incluyendo el sensor_id
        data = {
            "sensor_id":     request.id,
            "temperature":   request.temperature,
            "heart_rate":    request.heart_rate,
            "blood_pressure": request.blood_pressure
        }
        print("gRPC recibido:", data)
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
        return health_pb2.Response(status="OK")


async def run_grpc():
    await connect_mqtt()  # Espera la conexión MQTT
    
    # Usa el servidor asíncrono en lugar del síncrono
    server = grpc.aio.server()
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    server.add_insecure_port('[::]:50051')
    
    logging.info("Iniciando servidor gRPC en el puerto 50051")
    await server.start()  # Iniciar de forma asíncrona
    logging.info("Servidor gRPC iniciado y escuchando en puerto 50051")
    
    try:
        await server.wait_for_termination()  # Ahora sí es asíncrono
    except Exception as e:
        logging.error(f"Error en servidor gRPC: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_grpc())
