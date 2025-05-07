import grpc
import time
import random
import health_pb2
import health_pb2_grpc

def generate_health_data():
    return health_pb2.HealthData(
        temperature=round(random.uniform(36.0, 38.5), 1),
        heart_rate=random.randint(60, 100),
        blood_pressure=f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    )

def run():
    channel = grpc.insecure_channel('gateway:50051')
    stub = health_pb2_grpc.HealthServiceStub(channel)
    while True:
        data = generate_health_data()
        response = stub.SendHealthData(data)
        print(f"Enviado: {data} | Respuesta: {response.status}")
        time.sleep(5)

if __name__ == "__main__":
    run()
