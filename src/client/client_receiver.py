import paho.mqtt.client as mqtt
import json
import time
import threading
import temp_reader
from buzzer_led_handler import access_denied, access_granted
from client_requester import ZONE

BROKER_HOST = "10.108.33.121"
ZONE_NAME = "sauna"
TOPIC_NAME = "auth/response"

client = mqtt.Client()

display_refresh_interval = 2
display_paused = False


weather_displayer = temp_reader.OLEDWeatherDisplay()

def display_weather_data():
    while True:
        if not display_paused:
            weather_displayer.display_weather_data()
        time.sleep(display_refresh_interval)




def process_message(client, userdata, message):
    global display_paused

    message_decoded = json.loads(message.payload)
    print(message_decoded)

    if message_decoded["zoneId"] != ZONE:
        return

    # Tutaj logika w zalężoności czy autoryzacja udana czy nie,
    # jakieś buzzery etc
    authorized = message_decoded["accessGranted"]
    print(authorized)
    message = message_decoded["message"]

    if authorized is True:
        display_paused = True
        print(message)
        weather_displayer.display_text(message)
        access_granted()
        display_paused = False
    else:
        display_paused = True
        print(message)
        weather_displayer.display_text(message)
        access_denied()
        display_paused = False
 

def connect_to_broker():
    client.connect(BROKER_HOST)
    client.on_message = process_message

    client.loop_start()
    client.subscribe(TOPIC_NAME)


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    try:
        display_weather_thread = threading.Thread(target = display_weather_data())
        display_weather_thread.start()
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctrl+C received. Disconnecting from the broker and exiting.")
        disconnect_from_broker()

    disconnect_from_broker()


if __name__ == "__main__":
    print(f"starting clietn receiver in zone {ZONE_NAME}")
    run_receiver()
