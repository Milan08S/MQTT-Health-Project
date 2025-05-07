from concurrent import futures
import grpc
import json
import health_pb2
import health_pb2_grpc
import paho.mqtt.client as mqtt

MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "health/data"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

class HealthService(health_pb2_grpc.HealthServiceServicer):
    def SendHealthData(self, request, context):
        data = {
            "temperature": request.temperature,
            "heart_rate": request.heart_rate,
            "blood_pressure": request.blood_pressure
        }
        print("gRPC recibido:", data)
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
        return health_pb2.Response(status="OK")

def run_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC iniciado en el puerto 50051")
    server.start()
    server.wait_for_termination()
