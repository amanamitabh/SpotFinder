import json
import time
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import mysql.connector as mysql

load_dotenv()

server = os.getenv('SERVER')
db = os.getenv('DATABASE')
usr = os.getenv('USER')
pwd = os.getenv('PASSWORD')
port = os.getenv('PORT')

'''
con_obj = mysql.connect(host= server, database = db , username=usr, password=pwd)
mycur = con_obj.cursor()
'''

id = '47569a54-a0fa-47a5-a01a-946274c0d0e3'

client_telemetry_topic = id + '/spotfinder_gps'
client_name = id + 'mqtt_broker'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqtt_client.connect('test.mosquitto.org', 1883)

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    
    payload = json.loads(message.payload.decode())

    print("Message received:", payload)
    '''
    mycur.execute("UPDATE PARKING SET VACANT=%d, OCCUPIED=%d WHERE LAT=%s AND LON=%s;",
                   payload["vacant"], payload["occupied"], payload["lat"], payload["lon"])
    '''

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)