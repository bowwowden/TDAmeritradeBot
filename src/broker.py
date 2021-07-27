

class Broker():
    cash: int
    portfolio = list()

    def __init__(self):
        pass

    def set_starting_cash(self, cash):
        self.cash = cash

    def get_balance(self):
        return self.cash

    def order(self, position):
        self.deduct_cash(position)
        self.add_to_portfolio(position)

    def deduct_cash(self, position):
        self.cash = self.cash - (position.price * position.quantity)

    def add_to_portfolio(self, position):
        self.portfolio.append(position)

    def sell_position(self, position):
        self.profit_position(position)
        self.remove_from_portfolio()

    def profit_position(self, position):
        self.cash = self.cash + (position.price * position.quantity)

    def remove_from_portfolio(self):
        self.portfolio.pop(0)

    def has_position(self):
        if len(self.portfolio) is 0:
            return False
        return True
