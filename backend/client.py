import asyncio
import datetime
import json

import websockets

# obiekt na json i z niego stringify bo przez websocket
# mogą iść tylko str
# ważne żeby w wiadomości była data sparsowana na stringa
# istnieje pewien problem ze front otrzymuje 2 wiadomości
# jednocześnie z tym samym timestampem
# więc będziemy na froncie sprawdzać czy nie ma duplikatów

async def send(message: str):
    async with websockets.connect('ws://localhost:7001') as websocket:
        await websocket.send(message)

# invoke example
a = {
    "date": datetime.datetime.now().isoformat(),
    "card_uid": 'IDENTYFIKATOR KARTY',
    "reader": 1,
}

readyMSG = json.dumps(a)

asyncio.get_event_loop().run_until_complete(send(readyMSG))

