#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
import json
from db_handler import DB_HANDLER
from datetime import datetime, timedelta

POOL_ZONE = 2
SAUNA_ZONE = 3
PLAYGROUND_ZONE = 4

BROKER_HOST = "localhost"
TOPIC_LISTENER_NAME = "auth/request"
TOPIC_PUBLISHER_NAME = "auth/response"
client = mqtt.Client()

def card_valid_for_zone(card_id, zone_id):
    print(card_id)
    db_handler = DB_HANDLER()
    latest_ticket = db_handler.latest_ticket(card_id)
    message = ""
    if latest_ticket == None:
        message = f"No card with id: {card_id}"
        return {'accessGranted': False, 'message': message}
    
    valid_time = latest_ticket[5]
    purchase_time = datetime.strptime(latest_ticket[6], "%Y-%m-%d %H:%M:%S")
    valid_until = purchase_time + timedelta(minutes=valid_time)
    
    authorized_for_zone = latest_ticket[zone_id]
    
    if valid_until > datetime.now():
        message = f"The ticket is valid until: {valid_until}\n"
        if authorized_for_zone == 0:
            message = "Not valid for the requested zone:("
            return {'accessGranted': False, 'message': message}
        return {'accessGranted': True, 'message': message}
    else:
        message = f"The ticket was valid until: {valid_until}"
        return {'accessGranted': False, 'message': message}

def process_message(client, userdata, message):
    # W tej wiadomości powinno być card id
    message_decoded = json.loads(message.payload)
    print(f"received request to authorize: {message_decoded}")

    authorized = card_valid_for_zone(message_decoded['cardId'], message_decoded['accessZone'])
    json_data = json.dumps(authorized)
    # Odesłanie odpowiedzi na auth/response
    client.publish(TOPIC_PUBLISHER_NAME, json_data)


def connect_to_broker():
    client.connect(BROKER_HOST)
    client.on_message = process_message

    client.loop_start()
    client.subscribe(TOPIC_LISTENER_NAME)


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctrl+C received. Disconnecting from the broker and exiting.")
        disconnect_from_broker()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()

