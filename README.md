# Sistema de Monitoreo de Salud IoT

Un sistema de monitoreo de salud basado en IoT que recolecta, procesa y almacena datos médicos en tiempo real utilizando MQTT, PostgreSQL y Docker.

## Descripción del Proyecto

Este proyecto implementa una arquitectura de IoT para monitorear datos de salud como temperatura corporal, ritmo cardíaco y presión arterial. Los datos son capturados por sensores simulados, transmitidos a través de MQTT y almacenados en una base de datos PostgreSQL para su posterior análisis.

## Arquitectura

El sistema consta de los siguientes componentes:

- **Sensores**: Dispositivos simulados que generan datos de salud.
- **Gateway**: API REST, gRPC y WebSocket para recibir datos de los sensores.
- **MQTT Broker**: Implementado con Eclipse Mosquitto para la comunicación de mensajes.
- **Subscriber**: Cliente MQTT que recibe datos y los almacena en la base de datos.
- **Base de datos**: PostgreSQL para almacenamiento persistente de datos.
- **Monitor Web** (opcional): Interfaz web para visualizar los datos en tiempo real.

## Prerrequisitos

- Docker y Docker Compose
- Git (para clonar el repositorio)

## Estructura del Proyecto

```
mqtt-health-project/
├── docker-compose.yml
├── db/
├── gateway/
├── sensors/
├── subscriber/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── subscriber.py
└── mosquitto/
    ├── mosquitto.conf
    ├── data/
    └── log/
```

## Instalación y Ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/mqtt-health-project.git
   cd mqtt-health-project
   ```

2. Inicia los servicios con Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Verifica que todos los contenedores estén en ejecución:
   ```bash
   docker-compose ps
   ```

## Components

- [`gateway/`](./gateway): Servidor unificado que recibe datos vía REST, gRPC y WebSocket
- [`sensors/`](./sensors): Publicadores simulados de datos de salud
- [`subscriber/`](./subscriber): Persiste mensajes MQTT en PostgreSQL
- [`docker-compose.yml`](./docker-compose.yml): Lanza todos los servicios y gestiona la red

---

## Gateway

👉 [README detallado del gateway aquí](./gateway/README.md)

Resumen:
- Ejecuta REST en el puerto 5000
- Ejecuta gRPC en el puerto 50051
- Ejecuta WebSocket en el puerto 5002
- Publica en el tema MQTT `health/data`

---

## 📡 Sensors

👉 [README detallado de los sensores aquí](./sensors/README.md)

Resumen:
- Los sensores REST, gRPC y WebSocket se ejecutan en contenedores separados
- Cada uno envía periódicamente signos vitales simulados al gateway