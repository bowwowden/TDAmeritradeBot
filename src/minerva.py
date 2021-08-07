import json

import pandas as pd

from src.datainterface import DataInterface
from src.indicator import Indicator
from src.paperbroker import Broker
from src.position import Position


class Minerva:
    data_interface: DataInterface
    broker = Broker()
    _strategies = list()
    indicators = list()
    winning_positions = list()
    all_positions = list()
    total_trades: int = 0

    def __init__(self, data_interface: DataInterface):
        self.data_interface = data_interface
        self.broker.set_starting_cash(10000)

    def add_strategy(self, configuration):
        self._strategies.append(configuration)

    def get_strategies(self):
        return self._strategies

    def backtest_all_strategies(self):
        for i in range(0, len(self._strategies)):
            conf = self._strategies[i]
            self.backtest_strategy(conf)

    def backtest_strategy(self, conf):
        # self.strategy.data = self.load_data()
        # self.strategy.start(conf)
        pass

    def load_data(self):
        return self.data_interface.get_data()
