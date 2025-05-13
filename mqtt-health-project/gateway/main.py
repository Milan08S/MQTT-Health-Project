# gateway/main.py

from rest_server import app as rest_app
from grpc_server import run_grpc
from ws_server import run_ws
import asyncio
import threading
import logging
import socket

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_rest():
    logger.info("Iniciando servidor REST en puerto 5000...")
    rest_app.run(host='0.0.0.0', port=5000)

async def start_grpc_server():
    logger.info("Iniciando servidor gRPC...")
    try:
        await run_grpc()
    except OSError as e:
        if "Address already in use" in str(e) or "Only one usage of each socket address" in str(e):
            logger.error(f"ERROR: El puerto gRPC 50051 ya está en uso. {e}")
        else:
            logger.error(f"Error de red al iniciar servidor gRPC: {e}")
        raise
    except Exception as e:
        logger.error(f"Error al iniciar servidor gRPC: {e}", exc_info=True)
        raise

async def start_ws_server():
    logger.info("Iniciando servidor WebSocket...")
    try:
        await run_ws()
    except OSError as e:
        if "Address already in use" in str(e) or "Only one usage of each socket address" in str(e):
            logger.error(f"ERROR: El puerto WebSocket 5002 ya está en uso. {e}")
        else:
            logger.error(f"Error de red al iniciar servidor WebSocket: {e}")
        raise
    except Exception as e:
        logger.error(f"Error al iniciar servidor WebSocket: {e}", exc_info=True)
        raise

def run_async_servers():
    logger.info("Configurando servidores asíncronos...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Crear y ejecutar tareas
    try:
        grpc_task = loop.create_task(start_grpc_server())
        ws_task = loop.create_task(start_ws_server())
        
        # Ejecutar el bucle para siempre
        loop.run_forever()
    except Exception as e:
        logger.error(f"Error en servidores asíncronos: {e}")
        raise

if __name__ == "__main__":
    logger.info("Iniciando Gateway...")
    
    # Comprobar disponibilidad de puertos antes de iniciar
    def check_port(port, service_name):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("0.0.0.0", port))
            sock.close()
            return True
        except OSError:
            logger.warning(f"ADVERTENCIA: El puerto {port} para {service_name} ya está en uso")
            return False
    
    # Verificar puertos principales
    check_port(50051, "gRPC")
    check_port(5002, "WebSocket")
    
    # Iniciar servidor REST en un hilo
    rest_thread = threading.Thread(target=run_rest, daemon=True)
    rest_thread.start()
    
    # Iniciar servidores asíncronos (gRPC y WebSocket)
    run_async_servers()