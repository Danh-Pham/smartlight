import paho.mqtt.publish as publish
import paho.mqtt.client as client 
import serial
import json
import os
import time
from datetime import datetime
import psycopg2
import random

ON = True
device = '/dev/ttyS0'

database = "arduino-1.c9dhukv1umdc.us-west-1.rds.amazonaws.com"
port = 1883
broker = "172.20.10.5"
arduino = serial.Serial(device, 9600)
data = {
    "light_level": '0',
    "motion": '0'
}

command = {
    "command": ''    
}

#for communication with sensors
def on_connect_mqtt(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/device/light")
    client.subscribe("/device/motion")
    client.subscribe("/actuator/command")
    
def on_message_mqtt(client, userdata, msg):
    print(msg.topic + " "+ str(msg.payload))
    if str(msg.topic) == "/device/light":
        data["light_level"] = json.loads(msg.payload)["light_level"]
#         print(json.loads(msg.payload)["light_level"])
    if str(msg.topic) == "/device/motion":
        data["motion"] = json.loads(msg.payload)["detect_motion"]
#         print(json.loads(msg.payload)["detect_motion"])
    if str(msg.topic) == "/actuator/command":
        command["command"] = str(msg.payload)

client = client.Client()
client.on_connect = on_connect_mqtt
client.on_message = on_message_mqtt


def get_db_connection():
    conn = psycopg2.connect(
        host = database,
        database = "postgres",
        user = "postgres",
        password = "postgres")
    return conn

def push_data(light_level, motion, rgb_value, timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO arduino_data(light_level, motion, rgb_value, timestamp) VALUES (%s, %s, '%s', '%s')" % (light_level, motion, rgb_value, timestamp))
    conn.commit()
    cur.close()

#led_control function used for automation only 
def led_control(light, motion):
    led_state = 0
    print('led control ' + str(light) + str(motion))
    if motion == "0\r\n":
        arduino.write('0\n'.encode('utf-8'))
    
    if motion == "1\r\n":
        if light > 640:
            arduino.write('0\n'.encode('utf-8'))
            led_state = "0-0-0"
        if light >= 625 and light < 640:
            arduino.write('1\n'.encode('utf-8'))
            led_state = "255-0-0"
        if light >= 550 and light < 600:
            arduino.write('2\n'.encode('utf-8'))
            led_state = "0-255-0"
        if light >= 500 and light < 550:
            arduino.write('3\n'.encode('utf-8'))
            led_state = "0-0-255"
        if light >= 450 and light < 500:
            arduino.write('4\n'.encode('utf-8'))
            led_state = "255-0-255"
        if light >= 400 and light < 450:
            arduino.write('5\n'.encode('utf-8'))
            led_state = "255-255-0"
        if light >= 350 and light < 400:
            arduino.write('6\n'.encode('utf-8'))
            led_state = "0-255-255"
        if light >= 200:
            arduino.write('2\n'.encode('utf-8'))
            led_state = "255-255-255"
    return led_state

def led_control_by_command(command):
    rgb_value = '0'
    arduino.write(command.encode('utf-8'))
    str = command.encode('utf-8')
    if len(str) > 1:
        numbers = str.split(" ")
        str1 = numbers[1].split(',')
        red = str1[0]
        str2 = numbers[2].split(',')
        green = str2[0]
        blue = numbers[3]
        rgb_value = "%s-%s-%s" % (red, green, blue)
        print(rgb_value)
        print("")
        print(data["light_level"])
        print(data["motion"])
    return rgb_value

while True:
# Random for testing purpose
#     order = random.randrange(350, 650)
#     print(order)
#     led_control(order, 1)
#     push_data(460, 1, "255-255-0", datetime.now())
    client.loop_start()
    client.connect(broker, port, 60)
# For automation only
    rgb_value = led_control(data["light_level"], data["motion"])
# For control from web interface
#     rgb_value = led_control_by_command(command["command"])
    push_data(data["light_level"], data["motion"], rgb_value, datetime.now())
    client.loop_stop()
    
    

