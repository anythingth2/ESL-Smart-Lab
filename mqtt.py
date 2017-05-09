import paho.mqtt.client as mqtt
import thread


class mqtt_server:

    client=mqtt.Client()
    password_door=('1576')           #add password here!
    door_topic="/ESP/LED"           #change topic here!
    def on_connect(self,client,userdata,flags,rc):
        pass

    def on_message(self,client,userdata,msg):

        data=msg.payload.split(' ')
        username_message=data[0]
        message=""
        if msg.topic == self.door_topic and username_message != self.client._username and len(data)>1:
            message=data[1]
            if self.verify_password(message):
                self.client.publish(self.door_topic,self.client._username+" "+"1",2)
            else:
                self.client.publish(self.door_topic,self.client._username+" "+"0",2)

    def on_disconnect(self,client,userdata,msg):
        pass
    def __init__(self,address,port,username,password):
        self.client.on_connect=self.on_connect
        self.client.on_message=self.on_message
        self.client.on_disconnect=self.on_disconnect
        self.client.username_pw_set(username,password)
        self.client.connect(address,port,60)
        self.client.subscribe(self.door_topic,2)
        self.client.loop_forever()
    
    def __init__(self,address,port):
        self.client.on_connect=self.on_connect
        self.client.on_message=self.on_message
        self.client.on_disconnect=self.on_disconnect
        self.client.connect(address,port,60)
        self.client.subscribe(self.door_topic,2)
        self.client.loop_forever()
        
    def verify_password(self,input_password):
        for i in range(len(self.password_door)):
            if self.password_door[i]==input_password:
                return True
        return False

    

class door:
    mqtt_esl = mqtt_server('localhost','1883')
    def open_door():
        mqtt_esl.client.publish()
    
    
# address=raw_input("Input address : ")
# port = int(input("Input port : "))
# username=raw_input("Input username : ")
# password=raw_input("Input password : ")
