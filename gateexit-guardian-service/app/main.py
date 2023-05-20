import os
import random
import time
import signal
import sys

from paho.mqtt import client as mqtt_client
from loguru import logger

from message_helper import MessageHelper
from mqtt_topic_helper import MqttTopicHelper

broker = os.getenv('BROKER_ADDRESS', 'localhost')
port = 1883
client_id = "gateexit-guardian-service"

topic_helper = MqttTopicHelper('spectrum-grocers', 'fresh-frontier')
exit_topic = topic_helper.customer_departure()

message_helper = MessageHelper()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected with result code: {rc}")
        else:
            logger.info(f"Failed to connect, return code: {rc}")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(random.randint(2, 20))
        customer_id = random.randint(1, 10)
        product_ids = [random.randint(1, 100) for _ in range(random.randint(1, 10))]
        message = message_helper.customer_departure(customer_id, product_ids)
        result = client.publish(exit_topic, message)
        status = result[0]
        if status == 0:
            logger.info(f"Published message to topic {exit_topic}")
        else:
            logger.info(f"Failed to publish message to topic {exit_topic}")


def handle_exit(signum, frame):
    client.disconnect()
    logger.info("Gracefully shutting down...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    publish(client)
