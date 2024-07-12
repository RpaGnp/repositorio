import asyncio
import websockets
import json
import ssl
import os
from websockets import WebSocketServerProtocol

# Obtén la ruta del directorio donde se encuentra este script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construye las rutas a los archivos de certificados
cert_path = os.path.join(current_dir, 'ssl_certs', 'fullchain.pem')
key_path = os.path.join(current_dir, 'ssl_certs', 'privkey.pem')
print(f"este:  {key_path}")
print(f"este:  {cert_path}")



clients = []  # Lista para almacenar los clientes conectados

# Función para difundir la lista de clientes conectados
async def broadcast_clients_list():
    clients_list = [client['name_user'] for client in clients]
    message = json.dumps({'event': 'list_users', 'users': clients_list})
    for client in clients:
        try:
            await client['websocket'].send(message)
        except websockets.exceptions.ConnectionClosedError:
            pass  # Ignorar clientes que se desconectaron

async def handler(websocket, path):
    global clients

    try:
        while True:
            data = await websocket.recv()
            print("Datos recibidos:", data)

            try:
                json_data = json.loads(data)
                # Verifica la estructura del JSON
                if isinstance(json_data, dict) and 'event' in json_data and 'name' in json_data:
                    if isinstance(json_data['event'], str) and isinstance(json_data['name'], str):
                        # Si cumple con la estructura, procede a procesarlo
                        if json_data['event'] == 'connect':
                            clients.append({"name_user": json_data['name'], "websocket": websocket})
                            print(f"Nuevo cliente conectado: {json_data['name']}")
                            break  # Salimos del bucle ya que hemos procesado los datos válidos
                        else:
                            print("Evento no reconocido:", json_data['event'])
                    else:
                        print("Valores 'event' y 'name' deben ser cadenas de texto.")
                else:
                    print("JSON no cumple con la estructura esperada.") 
            except json.JSONDecodeError:
                print(f"No es un JSON válido: {data}")

        # Enviar la lista de clientes conectados a todos
        await broadcast_clients_list()

        while True:
            # Esperar mensajes del cliente web y procesarlos
            message_json = await websocket.recv()
            print("Mensaje recibido:", message_json)

            try:
                message_data = json.loads(message_json)
                recipient_name = message_data.get('recipient', None)
                if recipient_name:
                    # Buscar al destinatario en la lista de clientes
                    recipient = next((client for client in clients if client['name_user'] == recipient_name), None)
                    if recipient:
                        recipient_websocket = recipient['websocket']
                        await recipient_websocket.send(message_json)
                    else:
                        print(f"No se encontró al destinatario {recipient_name}.")
                else:
                    print("Mensaje no tiene destinatario especificado.")
            except json.JSONDecodeError:
                print("Mensaje recibido no es un JSON válido.")
            except websockets.exceptions.ConnectionClosedError:
                print("Conexión cerrada abruptamente.")

    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente desconectado (ClosedOK).")

    finally:
        clients = [client for client in clients if client['websocket'] != websocket]
        await broadcast_clients_list()  # Actualizar lista de clientes conectados

async def main():

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        ssl_context.load_cert_chain(
            certfile='C://Users//USER//JHON//TEST WEBSOCKETS//ssl//cert.pem',
            keyfile= 'C://Users//USER//JHON//TEST WEBSOCKETS//ssl//key.pem')
    except FileNotFoundError:
        print(f"Error: No se pueden encontrar los archivos de certificado.")
        print(f"Buscando en: {cert_path} y {key_path}")
        return
    except ssl.SSLError as e:
        print(f"Error al cargar los certificados: {e}")
        return

    try:
        async with websockets.serve(handler, "10.206.169.207", 8765, ssl=ssl_context):
            print("Servidor de WebSockets seguro levantado y escuchando en wss://10.206.169.207:8765")
            await asyncio.Future()  # Mantener el servidor en ejecución
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    asyncio.run(main())