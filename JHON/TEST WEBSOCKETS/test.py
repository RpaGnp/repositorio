import asyncio
import websockets
from websockets import WebSocketServerProtocol

clients = []  # Lista para almacenar los clientes conectados

# Función para difundir la lista de clientes conectados
async def broadcast_clients_list():
    clients_list = [client['name_user'] for client in clients]
    message = 'Clientes conectados: ' + ', '.join(clients_list)
    for client in clients:
        try:
            await client['websocket'].send(message)
        except websockets.exceptions.ConnectionClosedError:
            pass  # Ignorar clientes que se desconectaron

async def handler(websocket: WebSocketServerProtocol, path: str):
    global clients

    try:
        # Recibir el nombre del cliente desde el cliente web
        name = await websocket.recv()
        clients.append({"name_user": name, "websocket": websocket})
        print(f"Nuevo cliente conectado: {name}")

        # Enviar la lista de clientes conectados a todos
        await broadcast_clients_list()

        while True:
            try:
                # Esperar mensajes del cliente web y procesarlos
                message = await websocket.recv()
                print("message}")
                print(f"Mensaje recibido de {name}: {message}")

                recipient_name, message_text = message.split(':', 1) if ':' in message else (None, None)
                if recipient_name:
                    # Buscar al destinatario en la lista de clientes
                    recipient = next((client for client in clients if client['name_user'] == recipient_name), None)
                    if recipient:
                        recipient_websocket = recipient['websocket']
                        await recipient_websocket.send(f"Mensaje de {name}: {message_text}")
                    else:
                        print(f"No se encontró al destinatario {recipient_name}.")
                else:
                    print("Mensaje no tiene destinatario especificado o formato incorrecto.")
    
            except websockets.exceptions.ConnectionClosedError:
                print(f"Cliente {name} desconectado.")
                break
            except websockets.exceptions.ConnectionClosedOK:
                print(f"Cliente {name} desconectado (ClosedOK).")
                break

    except websockets.exceptions.ConnectionClosedError:
        print("Cliente desconectado abruptamente durante la conexión inicial.")
    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente desconectado (ClosedOK) durante la conexión inicial.")
    finally:
        clients = [client for client in clients if client['websocket'] != websocket]
        print(f"Cliente {name} eliminado de la lista de clientes.")
        await broadcast_clients_list()  # Actualizar lista de clientes conectados

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Servidor de WebSockets levantado y escuchando en ws://localhost:8765")
        await asyncio.Future()  # Mantener el servidor en ejecución

if __name__ == "__main__":
    asyncio.run(main())
