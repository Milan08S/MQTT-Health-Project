# MQTT-Health-Project
An IoT project where we simulate multiple health sensors and publish them with REST, gRPC and WebSockets using Mosquitto Broker with MQTT protocol to obtain the data and store it in a PostgreSQL database, simulating the publisher-subscriber method of the protocol, all integrated into a Docker Compose.

## Components

- [`gateway/`](./gateway): Unified server receiving data via REST, gRPC, and WebSocket
- [`sensors/`](./sensors): Simulated health data publishers
- [`subscriber/`](./subscriber): Persists MQTT messages into PostgreSQL
- [`docker-compose.yml`](./docker-compose.yml): Launches all services and manages networking

---

## Gateway

👉 [Detailed gateway README here](./gateway/README.md)

Summary:
- Runs REST on port 5000
- Runs gRPC on port 50051
- Runs WebSocket on port 5002
- Publishes to MQTT topic `health/data`

---

## 📡 Sensors

👉 [Detailed sensors README here](./sensors/README.md)

Summary:
- REST, gRPC, and WebSocket sensors run in separate containers
- Each sends simulated vital signs periodically to the gateway