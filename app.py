import time
import io
from counterfit_shims_picamera import PiCamera
from counterfit_connection import CounterFitConnection
import counterfit_shims_serial
import model

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
            model.predict()            
            time.sleep(10)