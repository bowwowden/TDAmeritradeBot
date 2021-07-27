

class Position():

    quantity: int = None
    price: int = None
    purchase_price: int = None
    sell_price: int = None

    def __init__(self):
        pass

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def set_price(self, price: int):
        self.price = price

    def set_purchase_price(self, price: int):
        self.purchase_price = price

    def set_sell_price(self, price: int):
        self.sell_price = price

    def is_winner(self):
        if self.sell_price > self.purchase_price:
            return True
        else:
            return False