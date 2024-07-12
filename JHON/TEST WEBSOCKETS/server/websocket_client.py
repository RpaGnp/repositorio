# websocket_client.py

import asyncio
import websockets
import json
from config.config import WS_SERVER_URI, RETRY_DELAY

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.connected = False
        self.websocket = None

    async def connect(self):
        while not self.connected:
            try:
                self.websocket = await websockets.connect(self.uri)
                self.connected = True
                print(f"Conectado al servidor WebSocket en {self.uri}.")
            except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError):
                print(f"No se pudo conectar al servidor WebSocket en {self.uri}. Reintentando...")
                await asyncio.sleep(RETRY_DELAY)

    async def send(self, message):
        if self.websocket and self.connected:
            await self.websocket.send(json.dumps(message))
            print(f"Mensaje enviado: {message}")

    async def receive(self):
        if self.websocket and self.connected:
            return await self.websocket.recv()

    async def listen(self):
        try:
            while self.connected:
                message = await self.receive()
                print(f"Mensaje recibido del servidor: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada por el servidor.")
            self.connected = False
