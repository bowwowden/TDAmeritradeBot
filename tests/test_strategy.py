import pytest

from src.broker import Broker
from src.datainterface import ExampleDataSource, DataSource
from src.indicator import Indicator
from src.indicators.macd import MACD
from src.signal import Signal


@pytest.fixture
def DataFeed():
    example_data = ExampleDataSource('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    dataframe = datasource.get_data()
    return dataframe


import pandas as pd


class TestStrategy():
    indicators = list()
    broker = Broker()
    buysig: Signal

    def __init__(self, data):
        self.data = data
        self.broker.set_starting_cash(10000)

    def add_indicator(self, ind: Indicator):
        self.indicators.append(ind)

    def add_buy_signal(self, signal):
        self.buysig = signal

    def start(self):
        stock_data = self.data
        for i in range(1, len(stock_data)):
            downswing: bool = False
            if pd.isna(stock_data['Downswing_Signal_Price'][i]):
                downswing = True

            upswing: bool = False
            if pd.isna(pd.isna(stock_data['Upswing_Signal_Price'][i])):
                upswing = True
                print()

    def next(self):
        pass

    def enter_position(self):
        pass

    def exit_position(self):
        pass


def test_strategy(DataFeed):
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    # Brokerage automatically uses 10000 in starting cash

    macd = MACD()
    strategy.add_indicator(macd)
    ma = strategy.indicators[0].get_crossover(strategy.data)
    # Add the MACD indicator data with buy and sell signals, which are crossovers, to the dataframe

    signal = {'indicator': 'macd', 'behavior': 'crossover', 'period': 15}
    strategy.add_buy_signal(signal)
    # Add the signal parameters to the strategy using preconfigured options

    # 1. Bullish: When the MACD line crosses over to the positive side and is above the middle line, buy into the stock after 15 minutes.
    # Exit the position after an hour (sell out of the position)
    # 2. Bearish: When the MACD line crosses over to the negative side and is below the middle line, sell short to open the position after 15 minutes
    # Exit (buy to close) the position after an hour

    strategy.start()
