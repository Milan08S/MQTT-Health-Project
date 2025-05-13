# IoT Gateway – REST + gRPC + WebSocket

This module contains the **unified gateway** for the IoT Health Monitoring system. It receives health data from simulated sensors over multiple protocols and publishes the data to an MQTT broker.

---

## Files

```text
gateway/
├── rest_server.py       # REST server using Flask
├── grpc_server.py       # gRPC server using grpcio
├── ws_server.py         # WebSocket server using websockets + asyncio
├── main.py              # Launches all 3 servers in parallel
├── requirements.txt     # Python dependencies
├── Dockerfile           # Image definition for the unified gateway
```
---

## How It Works

The gateway listens on three ports simultaneously, one for each protocol:

| Protocol   | Port   | Server File      |
|------------|--------|------------------|
| REST       | 5000   | `rest_server.py` |
| gRPC       | 50051  | `grpc_server.py` |
| WebSocket  | 5002   | `ws_server.py`   |

All servers are launched concurrently by `main.py` using Python’s `multiprocessing` module.

When data is received, the gateway:
- Logs the incoming message
- Publishes it to the MQTT broker on topic `health/data`

---

## How to Use with Docker

In `docker-compose.yml`, the gateway service should look like this:

```yaml
gateway:
  build: ./gateway
  container_name: gateway
  command: python main.py
  ports:
    - "5000:5000"    # REST
    - "50051:50051"  # gRPC
    - "5002:5002"    # WebSocket
  depends_on:
    - mqtt
  networks:
    - iot-net
```

## Dependencies

All required Python packages are listed in requirements.txt:

- flask
- paho-mqtt
- grpcio
- grpcio-tools
- websockets

You can install them manually for local testing using:

```bash
pip install -r requirements.txt
```


## Notes
- The MQTT broker must be available at host mqtt and port 1883 (as defined in docker-compose.yml).

- All incoming data, regardless of protocol, is published to the same topic:
health/data

- main.py uses Python’s multiprocessing module to run:

  - Flask server for REST

  - gRPC server using grpcio

  - WebSocket server using asyncio and websockets