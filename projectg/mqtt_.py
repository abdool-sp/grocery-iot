import paho.mqtt.client as mqtt


def get_topics():
    pass


def on_connect(client, userdata, rc):
    client.subscribe("/projectG/set_active/#")

def on_message(client, userdata, msg):
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("iot.eclipse.org", 1883, 60)

#client.loop_start()