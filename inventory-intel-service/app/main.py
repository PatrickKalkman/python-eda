import os
import signal
import time

import paho.mqtt.client as mqtt
from inventory import Inventory
from loguru import logger
from message_parser import MessageParser
from mqtt_topic_helper import MqttTopicHelper

# Define MQTT client ID and Broker Address
client_id = "inventory-intel-service"
message_broker_host = os.environ.get("BROKER_ADDRESS", "localhost")

# Initialize MQTT Helper
mqtt_helper = MqttTopicHelper("spectrum-grocers", "fresh-frontier")

# Initialize Message Parser
message_parser = MessageParser()

# Define Inventory
inventory = Inventory()


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT Broker: {message_broker_host} with result code: {rc}")
    client.subscribe(mqtt_helper.customer_departure())


def on_message(client, userdata, msg):
    message = message_parser.customer_departure(msg.payload)
    customer_id = message['customer_id']
    product_ids = message['product_ids']
    for product_id in product_ids:
        inventory.inventory[product_id]['stock'] -= 1
    logger.info(f"Inventory updated for customer {customer_id}.")


def log_inventory():
    while True:
        logger.info("Inventory Check:")
        for product_id, product_info in inventory.inventory.items():
            if int(product_info['stock']) < 100:
                logger.info(f"Id: {product_id}, Pr: {product_info['name']}," +
                            f"St: {product_info['stock']}")
        time.sleep(60)


def on_exit(signum, frame):
    logger.info("Received Exit Signal...Disconnecting from Broker")
    client.disconnect()
    exit(0)


# MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(message_broker_host)

# Handle exit signals
signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)

# Start MQTT client loop
client.loop_start()

# Log inventory every 30 seconds
log_inventory()
