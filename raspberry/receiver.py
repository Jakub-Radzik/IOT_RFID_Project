#!/usr/bin/env python3
import asyncio, websockets, datetime, neopixel, board, requests
import json, uuid, random, time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from config import *
from mfrc522 import MFRC522
# from datetime import datetime

BACKEND_API = 'http://localhost:5000'
WEBSOCKET_URL = 'ws://localhost:7001'

# obiekt na json i z niego stringify bo przez websocket
# mogą iść tylko str
# ważne żeby w w+iadomości była data sparsowana na stringa
# istnieje pewien problem ze front otrzymuje 2 wiadomości
# jednocześnie z tym samym timestampem
# więc będziemy na froncie sprawdzać czy nie ma duplikatów

# function
async def send(message: str):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        await websocket.send(message)


def get_json_data(log_id, date, card_uid, reader):
    data = {
            "id": log_id,
            "date": date,
            "card_uid": card_uid,
            "reader": int(reader)
        }   
    return json.dumps(data)

# broker
client = mqtt.Client()
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    print("Client connected")
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("card/info")


def disconnect_from_broker():
    # Disconnet the client.
    client.disconnect()
    print("Client disconnected")


def publish_response(response):
    client.publish("card/response", f'{response}')
    print('Published response')

def process_message(client, userdata, message):
    log_id, date, card_uid, reader = (str(message.payload.decode("utf-8"))).split('#')
    card_data = get_json_data(log_id, date, card_uid, reader)
    print(card_data)
    response = requests.post(f'{BACKEND_API}/logs/add', json=card_data)
    card_info = {
            "date": datetime.datetime.now().isoformat(),
            "card_uid": card_uid,
            "reader": int(reader),
        }
    readyMSG = json.dumps(card_info)
    
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError as ex:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(send(readyMSG))
    time.sleep(1)
    if response.status_code == 201:
        # przeslanie odpowiedniego response do raspberki oraz przez websocket
        publish_response('HTTP200')
    else:
        publish_response('HTTP400')

def main():
    connect_to_broker()

    user_input = input()
    while user_input != "quit":
        user_input = input()

    disconnect_from_broker()


if __name__ == "__main__":
    main()
