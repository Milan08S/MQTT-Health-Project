# Simulated Health Sensors

This module contains the **simulated health data publishers** for the IoT Health Monitoring system. Each sensor generates realistic vital signs and sends them to the gateway via a different protocol.

---

## Files

sensors/
├── rest_sensor.py # Sends data via REST (HTTP POST)
├── grpc_sensor.py # Sends data via gRPC
├── websocket_sensor.py # Sends data via WebSocket
├── proto/
│ └── health.proto # Protocol Buffers definition (for gRPC)
├── health_pb2.py # gRPC auto-generated messages
├── health_pb2_grpc.py # gRPC auto-generated service stubs
├── requirements.txt # Python dependencies
├── Dockerfile # Image definition for all sensors


---

## How It Works

Each sensor generates random health data such as:

- Temperature (36.0 – 38.5°C)
- Heart rate (60 – 100 bpm)
- Blood pressure (e.g. 120/80)

And sends it every 5 seconds to the gateway through its protocol.

| Sensor           | Protocol   | Target                               |
|------------------|------------|--------------------------------------|
| `rest_sensor.py` | REST       | `http://gateway:5000/data`           |
| `grpc_sensor.py` | gRPC       | `gateway:50051`                      |
| `websocket_sensor.py` | WebSocket | `ws://gateway:5002/ws`             |

---

## How to Use with Docker


Each sensor runs in its own container, using the same image. In `docker-compose.yml`, services are defined like:

```yaml
  sensor-rest:
    build: ./sensors
    command: python rest_sensor.py

  sensor-grpc:
    build: ./sensors
    command: python grpc_sensor.py

  sensor-ws:
    build: ./sensors
    command: python websocket_sensor.py
```

## Dependencies

All required Python packages are listed in requirements.txt:

- requests
- websocket-client
- grpcio
- grpcio-tools


You can install them manually for local testing using:

```bash
pip install -r requirements.txt
```

## Notes

The gRPC-related Python files (health_pb2.py and health_pb2_grpc.py) are generated from the .proto definition using the following command:

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/health.proto
```

If you don’t want to install grpcio-tools locally, you can generate these files using Docker:

```bash
docker run --rm -v $(pwd)/sensors:/app -w /app python:3.13-slim \
    sh -c "pip install grpcio-tools && python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/health.proto"
```



