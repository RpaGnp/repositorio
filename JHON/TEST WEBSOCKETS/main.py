# main.py

import asyncio
from botwebspckets import Bot
from server.websocket_client import WebSocketClient
from config.config import WS_SERVER_URI, BOT_NAME

async def main():
    ws_client = WebSocketClient(WS_SERVER_URI)
    bot = Bot(BOT_NAME, ws_client)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
