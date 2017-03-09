import paho.mqtt.client as mqtt
import thread


input_data=""
client=mqtt.Client()
def on_connect(client,userdata,flags,rc):
    print "Connected"
    client.subscribe("test",2)

def on_message(client,userdata,msg):
    print(str(msg.payload)+"")

def request_input():
    while True:
        input_data=raw_input()

def hive_mqtt():
    # client=mqtt.Client()
    print "Hive_mqtt is Connecting...."
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect("broker.mqttdashboard.com",1883,60)
    client.subscribe("test",2)
    client.loop_forever()


try:
    thread.start_new_thread(hive_mqtt,())
except :
    print "Failed to create hive_mqtt Thread"


while True : 
    input_data=raw_input()
    if input_data=="STOP":
        break
    elif input_data=="RECONNECT":
        client.reconnect()
    else:
        client.publish("test",input_data,2)
    



