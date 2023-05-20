import os
import signal

import paho.mqtt.client as mqtt
from customer_name_db import CustomerNameDb
from loguru import logger
from message_parser import MessageParser
from mqtt_topic_helper import MqttTopicHelper


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with result code: {rc}") 
    topic_helper = MqttTopicHelper('spectrum-grocers', 'fresh-frontier')
    client.subscribe(topic_helper.customer_arrival())


def on_message(client, userdata, msg):
    parser = MessageParser()
    customer_id = parser.get_customer_id(msg.payload)
    customer_name = CustomerNameDb().get_name(customer_id)
    logger.info(f"Welcome, {customer_name}")


def on_signal(signum, frame):
    logger.info("Received termination signal, disconnecting...")
    client.disconnect()


def main():
    global client
    client = mqtt.Client(client_id="hello-helper-service")
    client.on_connect = on_connect
    client.on_message = on_message

    # Register the signal handlers
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    message_broker_host = os.environ.get("BROKER_ADDRESS", "localhost")
    client.connect(message_broker_host, 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    main()
