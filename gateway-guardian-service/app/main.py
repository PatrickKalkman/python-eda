import os
import random
import signal
from threading import Event

from loguru import logger
from message_helper import MessageHelper
from mqtt_topic_helper import MqttTopicHelper
from paho.mqtt import client as mqtt_client

broker = os.getenv('BROKER_ADDRESS', 'localhost')
port = 1883
client_id = "gateway-guardian-service"
running = Event()  # Event object to replace the running flag


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    topic_helper = MqttTopicHelper("spectrum-grocers", "fresh-frontier")
    message_helper = MessageHelper()

    while not running.is_set():
        customer_id = random.randint(1, 10)
        topic = topic_helper.customer_arrival()
        message = message_helper.customer_arrival(customer_id)

        logger.info(f"Pub to {topic}: {message}")
        client.publish(topic, message)

        running.wait(random.randint(2, 20))

    client.disconnect()


# Handle Signals for Graceful Shutdown
def handle_signal(signum, frame):
    running.set()
    print("Gracefully shutting down...")


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == "__main__":
    client = connect_mqtt()
    client.loop_start()
    publish(client)
