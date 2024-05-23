import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522

BROKER_HOST = "10.108.33.121"
ZONE_NAME = "sauna"
TOPIC_NAME = "auth/request"

POOL_ZONE = 2
SAUNA_ZONE = 3
PLAYGROUND_ZONE = 4

ZONE = SAUNA_ZONE

client = mqtt.Client()

executing = True

def rfidRead():
    global executing
    MIFAREReader = MFRC522()
    last_scan = datetime.timestamp(datetime.now()) - 3
    while executing:
        if datetime.timestamp(datetime.now()) - last_scan > 3.0:
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    num = 0
                    for i in range(0, len(uid)):
                        num += uid[i] << (i*8)
                    print(f"Card read UID: {num}")
                    publish_data(TOPIC_NAME, ZONE, num)
       
                    last_scan = datetime.timestamp(datetime.now())

def publish_data(topic_name, access_zone, card_id):

    json_data = json.dumps({
        "accessZone" : access_zone,
        "cardId" : card_id 
    })

    client.publish(topic_name,  json_data)


def connect_to_broker():
    client.connect(BROKER_HOST)

def disconnect_from_broker():
    client.disconnect()

def run_sender():
    connect_to_broker()
    try:
        rfidRead()
    except KeyboardInterrupt:
        print("Ctrl+C received. Disconnecting from the broker and exiting.")
        disconnect_from_broker()


    disconnect_from_broker()


if __name__ == "__main__":
    print(f"Starting client auth requester in zone {ZONE_NAME}")
    run_sender()
