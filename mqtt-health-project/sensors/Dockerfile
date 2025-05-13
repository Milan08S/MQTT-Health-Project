FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos Python y protobuf
COPY *.py *.proto ./

# Compilar los archivos proto (solo si hay alguno)
RUN if ls *.proto 1> /dev/null 2>&1; then \
    pip install grpcio-tools && \
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto; \
    fi

# Copiar el script de entrada
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Usar el script de entrada como punto de entrada
CMD ["./entrypoint.sh"]