
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import threading
import requests 
import json

GPIO.setmode(GPIO.BCM)
pin = [21,20,16,19,26]
GPIO.setwarnings(False)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)


times = time.asctime(time.localtime(time.time()))
client = mqtt.Client()
passtime = ""


for i in range(len(pin)):
    GPIO.setup(pin[i], GPIO.IN)


def key():
    num = 0
    if (GPIO.input(pin[0]) == 1):num = num + 1
    if (GPIO.input(pin[1]) == 1):num = num + 2
    if (GPIO.input(pin[2]) == 1):num = num + 4
    if (GPIO.input(pin[3]) == 1):num = num + 8
    return num


def ticker():
    ticker = GPIO.input(pin[4])
    return ticker


def BeepT():
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(6, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(6, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(6, GPIO.LOW)
    time.sleep(1.8)
    GPIO.output(13, GPIO.LOW)


def BeepF():
    GPIO.output(6, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(6, GPIO.LOW)


# ////////////////////////////////////////////////////////////////MQTT
# def on_connect(client, userdata, rc):
#     print("Connected with result code ")
#     client.subscribe("/ESP/LED")
#
# def on_message(client, userdata, msg):
#     print(msg.topic + " " + msg.payload)
#
# def on_disconnect(client, userdata, rc):
#     print("Disconnected")
#
# def mqtts_publish(password ,time):
#
#     # if(client.connect):print "connect"
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.on_disconnect = on_disconnect
#     client.username_pw_set("RPITEST", "1234")
#     client.connect("m11.cloudmqtt.com", 12980, 60)
#     client.publish("/ESP/LED",passtime,2)
#     client.loop_forever()

# /////////////////////////////////////////////////////////////



if __name__ == '__main__':

    password = ""

    # try:
    #     thread_with_arg = threading.Thread(target = mqtts_publish,args = (password,time))
    #     thread_with_arg.start()
    # except:
    #     print "ERROR"


    while True:

        while ticker():
            GPIO.output(6, GPIO.LOW)
            pass
        inp = key()
        while not ticker():
            GPIO.output(6, GPIO.HIGH)
            pass
        time.sleep(0.1)


# /////////////// check pass
        if inp == 15 :
            # print password
            # if password == "1576":
            #     BeepT()
            #     passtime =  password + " ," +  times
            #     # client.publish("/ESP/LED",client._username + " "+ passtime , 2)
            #     print "OPEN"

            # else :
            #     BeepF()
            request = requests.post('http://localhost:8000/open_door',str(password))
            if request.content == 'True':
                BeepT()
                passtime =  password + " ," +  times
                print "OPEN"
            else:
                BeepF()
            password = ""
        else :
            password += str(inp)
