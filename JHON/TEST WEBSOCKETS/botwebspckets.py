import asyncio
import websockets
import json
import time

def proceso():
    cont = 0
    while True:
        cont+=1
        print (cont)
        time.sleep(2)
        if cont>=10:
            break


async def bot():
    uri = "ws://localhost:8765"  # Cambia esto si tu servidor está en una dirección diferente
    connected = False

    while not connected:
        try:
            async with websockets.connect(uri) as websocket:
                connected = True
                bot_name = input("ingresa nombre de bot: ")
                print(f"Bot {bot_name} conectado al servidor WebSocket.")

                # Enviar el nombre del bot para identificarlo en el servidor
                await websocket.send(bot_name)
                print("Mensaje de reporte enviado.")

                # Enviar un mensaje para reportar que el bot está conectado
                report_message = {
                    "recipient": "web",
                    "message": f"El {bot_name} se ha conectado",
                    "event": "mensaje"
                }
                await websocket.send(json.dumps(report_message))
                print("Mensaje de prueba enviado.")

                # Escuchar y procesar mensajes del servidor
                try:
                    while True:
                        message = await websocket.recv()
                        print(f"Mensaje recibido del servidor: {message}")
                        # Aquí puedes añadir lógica adicional para procesar los mensajes del servidor
                        message_data = json.loads(message)
                        message_data = message_data.get('message', None)
                        print(message_data)
                        if message_data == 'trabajo':
                            print(message_data)
                            report_message = {
                                "recipient": "web",
                                "message": f"El {bot_name} esta trabajando...",
                                "event": "mensaje"
                            }
                            await websocket.send(json.dumps(report_message))                            
                            proceso()

                            report_message = {
                                "recipient": "web",
                                "message": f"El {bot_name} finalizo",
                                "event": "mensaje"
                            }
                            await websocket.send(json.dumps(report_message))  

                        report_message = {
                            "recipient": "web",
                            "message": f"El {bot_name} esta libre",
                            "event": "mensaje"
                        }
                        await websocket.send(json.dumps(report_message))  

                except websockets.exceptions.ConnectionClosed:
                    print("Conexión cerrada por el servidor.")
                    connected = False
        except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError):
            print("No se pudo conectar al servidor WebSocket. Reintentando...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(bot())
