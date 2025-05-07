from multiprocessing import Process
from rest_server import run_rest
from grpc_server import run_grpc
from ws_server import run_ws
import asyncio

def start_ws():
    asyncio.run(run_ws())

if __name__ == "__main__":
    Process(target=run_rest).start()
    Process(target=run_grpc).start()
    Process(target=start_ws).start()
