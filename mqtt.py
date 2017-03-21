import paho.mqtt.client as mqtt
import thread


input_data=""
client=mqtt.Client()
def on_connect(client,userdata,flags,rc):
    print "#Connected "
def on_message(client,userdata,msg):
    print(msg.topic+" : "+msg.payload)
def on_disconnect(client,userdata,msg):
    print "#Disconnected"

def hive_mqtt(address,port):
    print "Hive_mqtt is Connecting...."
    client.on_connect=on_connect
    client.on_message=on_message
    client.on_disconnect=on_disconnect
    client.connect(address,port,60)
    client.loop_forever()

address=raw_input("Input address : ")
port = int(input("Input port : "))
client.username_pw_set("NodeTest","1234")
try:
    thread.start_new_thread(hive_mqtt,(address,port))
except :
    print ("Failed to create hive_mqtt Thread")

command = ["",""]

while True : 
    input_data=raw_input()
    command=input_data.split()
    if command[0]=="#STOP":
        break
    elif command[0] =="#RECONNECT":
        client.reconnect()
    elif command[0]=="#SUB":
        client.subscribe(command[1],2)
    elif command[0]=="#UNSUB":
        client.unsubscribe(command[1])
    else:
        client.publish(command[0],command[1],2)