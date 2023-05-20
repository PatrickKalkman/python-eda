import os
import paho.mqtt.client as mqtt
import time
import random
import signal
from loguru import logger

from mqtt_topic_helper import MqttTopicHelper
from message_helper import MessageHelper


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def handle_signal(signalNumber, frame):
    print("Received exit signal. Disconnecting...")
    client.disconnect()


client = mqtt.Client(client_id="gateway_guardian_service")


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def main():
    global client
    client.on_connect = on_connect

    message_broker_host = os.environ.get("BROKER_ADDRESS", "localhost")

    client.connect(message_broker_host, 1883, 60)

    topic_helper = MqttTopicHelper("spectrum-grocers", "fresh-frontier")
    message_helper = MessageHelper()


    client.loop_forever()


if __name__ == "__main__":
    main()
