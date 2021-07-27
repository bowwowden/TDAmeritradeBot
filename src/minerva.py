from src.datainterface import DataInterface
from src.strategy import StrategyInterface


class Minerva:
    data_interface: DataInterface
    strategy_interface: StrategyInterface
    _positions = list()

    def __init__(self, data_interface):
        self.data_interface = data_interface

    def load_data(self):
        return self.data_interface.get_data()

    def set_strategy(self, strategy_interface):
        self.strategy_interface = strategy_interface

    def backtest_strategy(self):
        dataframe = self.data_interface.get_data()
        if self.strategy_interface is not None:
            self.strategy_interface.backtest(dataframe)
            self.set_positions()
        else:
            print("Console log: There is no strategy currently loaded")

    def set_positions(self):
        _positions = self.strategy_interface.get_positions()

    def log_strategy_history(self):
        dataframe = self.data_interface.get_data()
        self.strategy_interface.get_positions()
