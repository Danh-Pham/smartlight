import serial
import pymysql
import time
import paho.mqtt.client as mqtt
import json
import requests

device ="/dev/ttyS0"
arduino = serial.Serial(device,9600)

port = 1883
sensor_data = {'detect_motion' : 0}
client = mqtt.Client()
client.connect("172.20.10.5")
client.loop_start()
try:
    while True:
        data = arduino.readline()
        sensor_data['detect_motion'] = data
        client.publish('/device/motion', json.dumps(sensor_data), 1)
        time.sleep(3)
except KeyboardInterrupt
    pass
client.loop_stop()
client.disconnect()