import json


class MessageParser:
    def parse_message(self, message):
        return json.loads(message)

    def get_customer_id(self, message):
        msg_dict = self.parse_message(message)
        return msg_dict.get('customer_id', None)

    def get_items(self, message):
        msg_dict = self.parse_message(message)
        return msg_dict.get('items', None)

    def get_item_id(self, message):
        msg_dict = self.parse_message(message)
        return msg_dict.get('item_id', None)

    def get_quantity(self, message):
        msg_dict = self.parse_message(message)
        return msg_dict.get('quantity', None)

    def get_timestamp(self, message):
        msg_dict = self.parse_message(message)
        return msg_dict.get('timestamp', None)
