#!/bin/bash
set -euo pipefail

# SENSOR_ID por defecto = hostname
: "${SENSOR_ID:=$(hostname)}"
echo "Iniciando sensor con ID: $SENSOR_ID"

# Forzar minúsculas
sensor_type="${SENSOR_TYPE:-}"
sensor_type="${sensor_type,,}"

# Si no viene SENSOR_TYPE, extraerlo del ID (parte tras último guión bajo)
if [ -z "$sensor_type" ]; then
  sensor_type="${SENSOR_ID##*_}"
  sensor_type="${sensor_type,,}"
  echo "Detectado tipo de sensor por ID: $sensor_type"
fi

case "$sensor_type" in
  rest)
    echo "Ejecutando sensor REST"
    exec python rest_sensor.py
    ;;
  ws)
    echo "Ejecutando sensor WebSocket"
    exec python websocket_sensor.py
    ;;
  grpc)
    echo "Ejecutando sensor gRPC"
    exec python grpc_sensor.py
    ;;
  *)
    echo >&2 "ERROR: Tipo de sensor inválido: '$sensor_type'"
    exit 1
    ;;
esac
