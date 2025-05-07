# gateway/rest_server.py
from flask import Flask, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "health/data"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

@app.route('/data', methods=['POST'])
def receive_data():
    # Extrae el JSON enviado por el sensor
    body = request.json
    # Construye el mensaje asegurando incluir sensor_id y métricas
    data = {
        "sensor_id":     body.get("id"),
        "temperature":   body["temperature"],
        "heart_rate":    body["heart_rate"],
        "blood_pressure": body["blood_pressure"]
    }
    print("REST recibido:", data)
    client.publish(MQTT_TOPIC, json.dumps(data))
    return '', 200

def run_rest():
    print("Servidor Rest iniciado en el puerto 5000")
    app.run(host="0.0.0.0", port=5000)
