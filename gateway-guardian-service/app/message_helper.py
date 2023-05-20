import json
from datetime import datetime


class MessageHelper:
    def _current_datetime(self):
        return datetime.now().isoformat()

    def customer_arrival(self, customer_id):
        return json.dumps({"timestamp": self._current_datetime(),
                           "customer_id": customer_id})

    def purchase_complete(self, customer_id, items):
        return json.dumps({"timestamp": self._current_datetime(),
                           "customer_id": customer_id, "items": items})

    def stock_update(self, item_id, quantity):
        return json.dumps({"timestamp": self._current_datetime(),
                           "item_id": item_id, "quantity": quantity})

    def restock_alert(self, item_id, quantity):
        return json.dumps({"timestamp": self._current_datetime(),
                           "item_id": item_id, "quantity": quantity})
