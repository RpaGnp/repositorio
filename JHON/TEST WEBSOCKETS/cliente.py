import asyncio
import websockets
import ssl

async def hello():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    uri = "wss://172.20.100.51:8765"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        name = input("¿Cuál es tu nombre? ")
        await websocket.send(f'{{"event": "connect", "name": "{name}"}}')
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())