class MqttTopicHelper:
    def __init__(self, chain_name, store_name):
        self.chain_name = chain_name
        self.store_name = store_name

    def customer_arrival(self):
        return f"{self.chain_name}/{self.store_name}/customer-arrival"

    def customer_departure(self):
        return f"{self.chain_name}/{self.store_name}/customer-departure"

    def display_welcome(self):
        return f"{self.chain_name}/{self.store_name}/display-welcome"

    def purchase_complete(self):
        return f"{self.chain_name}/{self.store_name}/purchase-complete"

    def stock_update(self):
        return f"{self.chain_name}/{self.store_name}/stock-update"

    def restock_alert(self):
        return f"{self.chain_name}/{self.store_name}/restock-alert"
