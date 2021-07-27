class Paper():

    balance: int
    positions: list()

    def __init__(self):
        pass

    def calculate_balance(self, positions: list([int, str])) -> int:
        profit: int = 0
        for position in positions:
            signal = position[1]
            # Upswing Buy Calls
            if signal == 'Buy':
                profit -= position[0]
            # Downswing Buy Puts
            if signal == 'Sell':
                profit += position[0]
        self.balance += profit
        return profit

