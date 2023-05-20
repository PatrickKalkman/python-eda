from faker import Faker


class Inventory:
    def __init__(self):
        self.fake = Faker()
        self.inventory = self._generate_inventory()

    def _generate_inventory(self):
        inventory = {}
        for i in range(1, 101):  # generate 100 products
            inventory[i] = {'name': self.fake.commerce.product(), 'stock': 100}
        return inventory
