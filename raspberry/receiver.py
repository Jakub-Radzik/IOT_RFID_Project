import asyncio, websockets, datetime, neopixel, board, requests
import json, uuid, random, time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from config import *
from mfrc522 import MFRC522
from datetime import datetime

BACKEND_API = 'http://localhost:5000'

# obiekt na json i z niego stringify bo przez websocket
# mogą iść tylko str
# ważne żeby w w+iadomości była data sparsowana na stringa
# istnieje pewien problem ze front otrzymuje 2 wiadomości
# jednocześnie z tym samym timestampem
# więc będziemy na froncie sprawdzać czy nie ma duplikatów

# function
async def send(message: str):
    async with websockets.connect('ws://localhost:7001') as websocket:
        await websocket.send(message)

# invoke example
asyncio.get_event_loop().run_until_complete(send(str(datetime.datetime.now())))


def get_json_data(log_id, date, card_uid, reader):
    data = {
            "log_id": log_id,
            "date": date,
            "card_uid": card_uid,
            "reader": reader
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
    # save to db
    # if successful publish response, send to ws and backend
    card_data = get_json_data(log_id, date, card_uid, reader)
    response = requests.post('{BACKEND_API}/logs/add', data=card_data)
    if response.status_code == 200:
        # przeslanie odpowiedniego response do raspberki oraz przez websocket
        publish_response('HTTP200')
        send(card_data)
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
