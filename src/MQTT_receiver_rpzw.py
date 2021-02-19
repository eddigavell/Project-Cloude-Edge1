import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import gpiozero

digital_out = gpiozero.DigitalOutputDevice(23, active_high=True, initial_value=False, pin_factory=None)
MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
sub_topic = 'tjaru/'
pub_topic = 'tjaru/status'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected to {MQTT_SERVER}:{MQTT_PORT} with result code ' + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(sub_topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + ":" + str(msg.payload.decode()))
    # more callbacks, etc
    if msg.payload == 'LAMP ON'.encode():
        digital_out.on()
        publish.single(pub_topic, "LAMP IS ON!", 2, True, hostname=MQTT_SERVER)
    elif msg.payload == 'Lamp off'.encode():
        digital_out.off()
        publish.single(pub_topic, "LAMP IS OFF!", 2, True, hostname=MQTT_SERVER)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
