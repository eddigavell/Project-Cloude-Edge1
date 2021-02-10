import paho.mqtt.client as mqtt

# Client data
client_id = 'RSPPI switch1'
broker_ip = 'broker.mqttdashboard.com'
broker_port = 1883

# Topic data
sub_topic = 'tjaru/hej/vadheterdu'
pub_topic = 'tjaru/hej/vadheterdu/status'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected to {broker_ip}:{broker_port}, with result code: {str(rc)}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'{msg.topic}: {str(msg.payload)}')
    if msg.payload == 'katt'.encode():
        print(f'Message was katt')
    else:
        print(f'Message was NOT katt')


client = mqtt.Client(client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, broker_port, 60)
client.subscribe(sub_topic)
msg_to_pub = client_id + " are online and listening to " + sub_topic
client.publish(pub_topic, msg_to_pub, 2, True)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
