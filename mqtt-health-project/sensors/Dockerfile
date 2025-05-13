# 1. Usa una versión real de Python (3.13 aún no existe)
FROM python:3.10-slim

WORKDIR /app

# 3. Copia y bloquea la instalación de dependencias en un solo layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 4. Copia sólo lo necesario (mantiene el contexto limpio)
COPY *.py *.proto entrypoint.sh ./

# 5. Compila los .proto *antes* de instalar grpcio-tools
RUN if ls *.proto 1> /dev/null 2>&1; then \
      pip install --no-cache-dir grpcio-tools && \
      python -m grpc_tools.protoc -I. \
        --python_out=. --grpc_python_out=. *.proto; \
    fi

# 6. Asegura permisos de ejecución
RUN chmod +x entrypoint.sh

# 7. Expone puertos (ajusta según tu sensor)
# EXPOSE 50051 8080

# 8. Añade un HEALTHCHECK básico (opcional)
HEALTHCHECK --interval=30s --timeout=5s \
  CMD pgrep -f websocket_sensor.py || exit 1

# 9. Usa ENTRYPOINT + CMD para separar lógica y argumentos
ENTRYPOINT ["./entrypoint.sh"]
CMD []
