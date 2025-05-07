import os, json
import paho.mqtt.client as mqtt
import psycopg2

# variables desde entorno
PG_HOST     = os.getenv("PG_HOST","postgres-db")
PG_PORT     = os.getenv("PG_PORT",5432)
PG_DB       = os.getenv("PG_DATABASE","healthdata")
PG_USER     = os.getenv("PG_USER","iotuser")
PG_PASS     = os.getenv("PG_PASS","iotpassword")
MQTT_BROKER = os.getenv("MQTT_BROKER","mqtt")
MQTT_PORT   = int(os.getenv("MQTT_PORT",1883))
MQTT_TOPIC  = os.getenv("MQTT_TOPIC","health/data")

# conexión a PostgreSQL
conn = psycopg2.connect(host=PG_HOST,port=PG_PORT,dbname=PG_DB,user=PG_USER,password=PG_PASS)
conn.autocommit=True
cur = conn.cursor()

# Crear la tabla si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS health_readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    temperature FLOAT,
    heart_rate INTEGER,
    blood_pressure VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
print("Tabla health_readings verificada/creada")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    print("Subscriber conectado a MQTT, suscrito a", MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    cur.execute(
      "INSERT INTO health_readings(sensor_id, temperature, heart_rate, blood_pressure) VALUES(%s,%s,%s,%s)",
      (payload["sensor_id"], payload["temperature"], payload["heart_rate"], payload["blood_pressure"])
    )
    print("Guardado en BD:", payload)

# Nota: La siguiente línea generará una advertencia de deprecación, pero funciona
# Para versiones más recientes de paho-mqtt, deberías usar:
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()