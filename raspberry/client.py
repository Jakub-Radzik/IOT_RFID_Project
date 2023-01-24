import asyncio, websockets, datetime, neopixel, board
import json, uuid, random, time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from config import *
from mfrc522 import MFRC522
from datetime import datetime


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


class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 128, 0)
    yellow = (255, 255, 0)


class LedHandler:
    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.colors = [Color.black for _ in range(8)]
        self.update_all()

    def update_all(self):
        for i in range(8):
            self.pixels[i] = self.colors[i]
        self.pixels.show()

    def clear(self):
        self.set_color_all(Color.black)
        self.update_all()

    def successful_reading(self):
        self.colors = [Color.green for _ in range(8)]
        self.update_all()

    def failed_reading(self):
        self.colors = [Color.red for _ in range(8)]
        self.update_all()



class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.was_read: bool = False
        self.last_detection: datetime = None
        self.last_card_uid = None
        self.log_id = None  
        self.machine_id = uuid.getnode() #  adres mac maliny

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                new_time = datetime.datetime.now()
                if not self.was_read:
                    self.was_read = True
                    self.last_detection = new_time
                    self.last_card_uid = uid
                    self.log_id = random.randint(0, 2**31-1)
                    return self.was_read
                return self.was_read
        else:
            self.was_read = False
        return self.was_read


    def log(self):
        data = {
            "log_id": str(self.log_id),
            "date": self.last_detection.strftime("%d-%m-%Y %H:%M:%S"),
            "card_uid": str(self.last_card_uid),
            "reader": str(self.machine_id)
        }
        return json.dumps(data)



def play_sound_success():
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin, GPIO.LOW)
    time.sleep(0.3)

def play_sound_failure():
    for i in range(3):
        GPIO.output(buzzerPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(0.1)


#   zapis do bazy? połączenie z frontem / backiem? - tbd