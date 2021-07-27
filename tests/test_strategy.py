import json
import pandas as pd

import pytest

from src.broker import Broker
from src.datainterface import ExampleDataSource, DataSource
from src.indicator import Indicator
from src.indicators.macd import MACD
from src.position import Position


@pytest.fixture
def DataFeed():
    example_data = ExampleDataSource('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    dataframe = datasource.get_data()
    return dataframe


class TestStrategy():
    indicators = list()
    broker = Broker()

    def __init__(self, data: pd):
        self.data = self.set_dataframe_to_json(data)
        self.broker.set_starting_cash(10000)

    def print_stock_data(self):
        for candlestick in self.data:
            print(candlestick)

    def set_dataframe_to_json(self, data: pd):
        data = data.to_json(orient='records')
        data = json.loads(data)
        return data

    def add_indicator(self, indicator: Indicator):
        self.indicators.append(indicator)

    def start(self):
        stock_data = self.data
        length = len(stock_data)
        for i in range(0, length):

            position: Position = Position()
            candlestick = stock_data[i]

            price: int = 0
            if (i+3) < length:
                # 15 minutes
                price = stock_data[i+3]['close']

            # Behavior,
            # Time
            # Buy one stock after 15 minutes
            if candlestick['crossover'] == 'Upswing':
                position.set_quantity(1)
                position.set_price(price)
                self.enter_position(position)

                # 1 hour after 15 minutes = 5 * 12

            elif candlestick['crossover'] == 'Downswing':
                position.set_quantity(1)
                position.set_price(price)
                self.exit_position(position)

            self.log(position, candlestick)

    def log(self, position: Position, candlestick):
        balance: str = str(self.broker.get_balance())
        position: str = str(position.price)
        stock_price = str(candlestick['close'])
        trend = str(candlestick['crossover'])

        print("Balance: " + balance
              + " | Position: " + position
              + " | Close: " + stock_price
              + " | Trend: " + trend)

    def enter_position(self, position):
        self.broker.order(position)

    def exit_position(self, position):
        if self.broker.has_position():
            self.broker.sell_position(position)

    def stop(self):
        balance = str(self.broker.get_balance())
        print("Final Balance: " + balance
              + " | Win Rate: ")


def test_strategy_print(DataFeed):
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    strategy.print_stock_data()

    assert True


def test_strategy_indicator_to_json(DataFeed):
    macd: MACD = MACD()
    dataframe = macd.get_macd_indicators(DataFeed)
    strategy: TestStrategy = TestStrategy(data=dataframe)
    strategy.print_stock_data()

    assert type(strategy.data) is list


def test_strategy_log_crossover_points(DataFeed):
    macd: MACD = MACD()
    dataframe = macd.get_crossover(DataFeed)
    strategy: TestStrategy = TestStrategy(data=dataframe)
    strategy.print_stock_data()


def test_macd_bullish_bearish_strategy(DataFeed):
    macd: MACD = MACD()
    dataframe = macd.get_crossover(DataFeed)

    strategy: TestStrategy = TestStrategy(data=DataFeed)
    # Brokerage automatically uses 10000 in starting cash
    # Add the signal parameters to the strategy using preconfigured options

    # 1. Bullish: When the MACD line crosses over to the positive side and is above the middle line, buy into the stock after 15 minutes.
    # Exit the position after an hour (sell out of the position)
    # 2. Bearish: When the MACD line crosses over to the negative side and is below the middle line, sell short to open the position after 15 minutes
    # Exit (buy to close) the position after an hour

    strategy.start()
    strategy.stop()
