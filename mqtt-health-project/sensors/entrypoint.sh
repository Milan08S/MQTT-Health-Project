#!/bin/bash

# Si no se ha establecido SENSOR_ID, usar el hostname del contenedor
if [ -z "$SENSOR_ID" ]; then
  export SENSOR_ID=$(hostname)
fi

echo "Iniciando sensor con ID: $SENSOR_ID"

# Verificar el tipo de sensor a ejecutar
case "$SENSOR_TYPE" in
  "rest")
    echo "Ejecutando sensor REST"
    python rest_sensor.py
    ;;
  "ws")
    echo "Ejecutando sensor WebSocket"
    python websocket_sensor.py
    ;;
  "grpc")
    echo "Ejecutando sensor gRPC"
    python grpc_sensor.py
    ;;
  *)
    # Si no se especifica un tipo, intentar detectar qué script ejecutar
    # basado en el ID del sensor
    if [[ "$SENSOR_ID" == *"REST"* ]]; then
      echo "Detectando tipo REST basado en ID del sensor: $SENSOR_ID"
      python rest_sensor.py
    elif [[ "$SENSOR_ID" == *"WS"* ]]; then
      echo "Detectando tipo WS basado en ID del sensor: $SENSOR_ID"
      python websocket_sensor.py
    elif [[ "$SENSOR_ID" == *"GRPC"* ]]; then
      echo "Detectando tipo GRPC basado en ID del sensor: $SENSOR_ID"
      python grpc_sensor.py
    else
      echo "No se pudo determinar el tipo de sensor. Ejecutando sensor REST por defecto."
      python rest_sensor.py
    fi
    ;;
esac