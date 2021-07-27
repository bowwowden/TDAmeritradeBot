from src.strategy import Strategy


class Bot:

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def simulate_strategy(self):
        self.strategy.backtest_strategy()

    def plot_graph(self):
        self.strategy.plot_data()