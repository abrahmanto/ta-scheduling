# python3.6

import random

from paho.mqtt import client as mqtt_client
from flask_mqtt import Mqtt as mqttFlask


from pymongo import MongoClient


from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

import json

# run : python pahoSub.py
# pip install --upgrade setuptools

broker = '192.168.195.203'
port = 1883
topic = "python/mqtt/TESTBrokerBaruBro"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connectKeDatab():
                  linkDB = "mongodb://dbusr:dbusrpasswd@192.168.195.203:27017/backend?authSource=admin&w=1"
                  dbClient = MongoClient(linkDB)
                  return dbClient['piiclone']

def cariDiDatab(msg):
    DBKoleksi = connectKeDatab()
    DBTampung = DBKoleksi['form_penilaian']
    TASKCari = DBTampung.find({"pid": msg})
    TASKAntri = []
    for TASKkonfirm in TASKCari:
        print(TASKkonfirm)
        TASKAntri.append(TASKkonfirm)

    


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"RECEIVED `{msg.payload.decode()}` FROM `{msg.topic}` TOPIC")
        meseg = json.loads(msg.payload.decode())
        print("NEW TASK! \n", meseg['pid'])
        cariDiDatab(meseg['pid'])

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
