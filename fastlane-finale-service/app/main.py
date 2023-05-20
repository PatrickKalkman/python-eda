import os
import random
import signal
import sys
import time

from loguru import logger
from message_helper import MessageHelper
from message_parser import MessageParser
from mqtt_topic_helper import MqttTopicHelper
from paho.mqtt import client as mqtt_client


class ProductPricing:
    def __init__(self):
        self.prices = {i: round(random.uniform(1, 20), 2) for i in range(1, 101)}

    def get_price(self, product_id):
        return self.prices.get(product_id, 0)


broker = os.getenv('BROKER_ADDRESS', 'localhost')
port = 1883
client_id = "fastlane_finale_service"
topic_helper = MqttTopicHelper("spectrum-grocers", "fresh-frontier")
message_helper = MessageHelper()
message_parser = MessageParser()
product_pricing = ProductPricing()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client):
    def on_message(client, userdata, msg):
        customer_departure = message_parser.customer_departure(msg.payload)
        total_price = 0
        for product_id in customer_departure['product_ids']:
            total_price += product_pricing.get_price(product_id)
        payment_message = message_helper.payment_due(customer_departure['customer_id'],
                                                     total_price)
        client.publish(topic_helper.payment_due(), payment_message)

        logger.info(f"Payment due for customer {customer_departure['customer_id']}:" +
                    f" ${total_price:.2f}")

    client.subscribe(topic_helper.customer_departure())
    client.on_message = on_message


def handle_signal(signum, frame):
    logger.info("Gracefully shutting down...")
    client.disconnect()
    sys.exit(0)


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    while True:
        time.sleep(1)  # just to prevent the script from ending


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


if __name__ == "__main__":
    run()
