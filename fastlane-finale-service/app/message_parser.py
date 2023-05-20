import json


class MessageParser:
    def customer_arrival(self, message):
        data = json.loads(message)
        return {'timestamp': data['timestamp'], 'customer_id': data['customer_id']}

    def customer_departure(self, message):
        data = json.loads(message)
        return {'timestamp': data['timestamp'], 'customer_id': data['customer_id'],
                'product_ids': data['product_ids']}
