import asyncio
import websockets

async def ouvir_notificacoes():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("✅ Ligado ao WebSocket. À espera de notificações...")
        while True:
            msg = await websocket.recv()
            print("🔔 Notificação:", msg)

asyncio.run(ouvir_notificacoes())
