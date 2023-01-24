import datetime, neopixel, board
import uuid, random, time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from config import *
from mfrc522 import MFRC522
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

BOUNCE_TIME = 100

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

    def wait_reading(self):
        self.colors = [Color.yellow for _ in range(8)]
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

    def get_data(self):
        data = {
            "log_id": str(self.log_id),
            "date": self.last_detection.strftime("%d-%m-%Y %H:%M:%S"),
            "card_uid": str(self.last_card_uid),
            "reader": str(self.machine_id)
        }
        return data


def play_sound_success():
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(buzzerPin, GPIO.LOW)


def play_sound_failure():
    for i in range(3):
        GPIO.output(buzzerPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(0.1)

execute = True
is_not_waiting_for_response = False

# OLED
background = Image.new("RGB", (96, 64), "BLACK")
draw = ImageDraw.Draw(background)
font = ImageFont.truetype('./lib/oled/Font.ttf', 10)
disp = SSD1331.SSD1331()

def oled_show():
    disp.ShowImage(background, 0, 0)


def show_card_message():
    erase_oled()
    draw.text((25, 10), 'Przyloz', font=font, fill="WHITE")
    draw.text((30, 25), 'Karte', font=font, fill="WHITE")
    oled_show()


def erase_oled():
    draw.rectangle(((0, 0), (96, 64)), fill="BLACK")
    

#uzycie przycisku, wylaczenie programu
def redButtonPressedCallback(channel):
    global execute
    execute = False

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
    client.subscribe("card/response")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()
    print("Client disconnected")


def publish_card_log(log_id, date, card_uid, reader):
    client.publish("card/info", f'{log_id}#{date}#{card_uid}#{reader}')
    print('Published card read info')


def process_message(client, userdata, message):
    response = (str(message.payload.decode("utf-8")))
    if response == 'HTTP200':
        led_handler.successful_reading()
        play_sound_success()
    else:
        led_handler.failed_reading()
        play_sound_failure()
    show_card_message()
    global is_waiting_for_response
    is_waiting_for_response = False


# led handler
led_handler = LedHandler()

def readCardInLoop():
    rfid_handler = RFIDHandler()
    while execute and not is_waiting_for_response:
        readCardValue = rfid_handler.read()
        if readCardValue:
            erase_oled()
            oled_show()
            global is_waiting_for_response
            is_waiting_for_response = True
            led_handler.wait_reading()
            log_id, date, card_uid, reader = rfid_handler.get_data()
            publish_card_log(log_id, date, card_uid, reader)
            # czekanie na message od drugiej maliny


def main():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonPressedCallback, bouncetime=BOUNCE_TIME)
    disp.Init()
    disp.clear()
    show_card_message()
    connect_to_broker()
    readCardInLoop()
    disconnect_from_broker()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
