import time
import io
import json
import pynmea2
import paho.mqtt.client as mqtt
from counterfit_shims_picamera import PiCamera
from counterfit_connection import CounterFitConnection
import counterfit_shims_serial
import model


def print_gps_data(line):
    print(line.rstrip())


def pad_coordinate(raw_value, direction):
    # Pad coordinates with leading zeros to match standard format

    if not raw_value:
        return None
    if direction in ['N', 'S']:
        return raw_value.zfill(9)
    elif direction in ['E', 'W']:
        return raw_value.zfill(10)
    return raw_value



def convert_to_decimal(raw_value, direction):
    if not raw_value:
        return None

    raw_value = raw_value.strip()

    # Determine if this is latitude or longitude based on direction
    # Latitudes: N/S → degrees are 2 digits
    # Longitudes: E/W → degrees are 3 digits
    if direction in ['N', 'S']:
        degree_len = 2
    elif direction in ['E', 'W']:
        degree_len = 3
    else:
        return None  # Invalid direction

    # Split into degrees and minutes
    degrees = float(raw_value[:degree_len])
    minutes = float(raw_value[degree_len:])

    decimal = degrees + (minutes / 60)

    # Apply sign for S/W
    if direction in ['S', 'W']:
        decimal *= -1

    return decimal


# Setting up device for MQTT
id = '47569a54-a0fa-47a5-a01a-946274c0d0e3'
client_name = id + 'cam_client_1'
client_telemetry_topic = id + '/spotfinder_gps'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqtt_client.connect('test.mosquitto.org', 1883)
mqtt_client.loop_start()
print("MQTT connected!")

# Setting up connections with camera and gps modules
serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
CounterFitConnection.init('127.0.0.1', 5000)
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 0


# Infinite loop to continuously capture images, classify and send data
while True:
    line = serial.readline().decode('utf-8')

    # Capture image from Picamera and store it in memory
    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    image.seek(0)

    if not line:
        continue

    print_gps_data(line)

    with open('image.jpg', 'wb') as image_file:
        image_file.write(image.getvalue())
    stats = model.predict()

    # Parse GPS data
    msg = pynmea2.parse(line)
    stats["lat"] = round(msg.latitude, 9)
    stats["lon"] = round(msg.longitude, 9)
    stats["client_name"] = client_name


    data = json.dumps(stats)
    print("Sending telemetry ", data)
    mqtt_client.publish(client_telemetry_topic, data)            
    time.sleep(10)