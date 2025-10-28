import time
import io
import json
import paho.mqtt.client as mqtt
from counterfit_shims_picamera import PiCamera
from counterfit_connection import CounterFitConnection
import counterfit_shims_serial
import model

# Setting up device for MQTT

id = '47569a54-a0fa-47a5-a01a-946274c0d0e3'
client_name = id + 'cam_client_1'
client_telemetry_topic = id + '/spotfinder_gps'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

# Setting up connections with camera and gps modules

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
CounterFitConnection.init('127.0.0.1', 5000)
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 0

def print_gps_data(line):
    print(line.rstrip())

while True:
    line = serial.readline().decode('utf-8')
    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    image.seek(0)

    while len(line) > 0:
        print_gps_data(line)
        line = serial.readline().decode('utf-8')
        with open('image.jpg', 'wb') as image_file:
            image_file.write(image.read())
            stats = model.predict()

        stats["lat"] = "110.229N"
        stats["lon"] = "251.001E"
        data = json.dumps(stats)
        print("Sending telemetry ", data)
        mqtt_client.publish(client_telemetry_topic, data)            
        time.sleep(10)