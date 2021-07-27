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
    total_trades: int = 0
    winning_positions = list()
    all_positions = list()

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

    def start(self, configuration):
        stock_data = self.data

        enter_time: int = configuration['enter_time']
        exit_time: int = configuration['exit_time']
        buy_position_index = 0
        exit_position_index = 0
        sell_position_index = 0

        length = len(stock_data)
        for i in range(0, length):

            position: Position = Position()
            candlestick = stock_data[i]
            price: int = stock_data[i]['close']

            # Trend Flag
            if candlestick['crossover'] == 'Upswing':
                # 15 minutes later
                buy_position_index = i + enter_time
                # 1 hour later
                exit_position_index = buy_position_index + exit_time

            # Buy After 15 Minutes
            if i == buy_position_index and i != 0:
                position.set_quantity(1)
                position.set_price(price)
                position.set_purchase_price(price)
                self.enter_position(position)

            # Trend Flag
            if candlestick['crossover'] == 'Downswing':
                # sell after 5 minutes
                sell_position_index = i + 3

            # If 15 minutes after downswing or 1 hour entering position
            if (i == sell_position_index or i == exit_position_index ) and self.broker.has_position():
                position.set_quantity(1)
                position.set_price(price)
                position.set_sell_price(price)
                self.exit_position(position)

            # check to exit position
            if i == length:
                position.set_quantity(1)
                position.set_price(price)
                position.set_sell_price(price)
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
              + " | Trend: " + trend
              + " | Number of Positions: " + str(len(self.broker.portfolio)))

    def enter_position(self, position):
        self.all_positions.append(position)
        self.broker.order(position)

    def exit_position(self, position):
        if self.broker.has_position():
            if self.check_if_position_wins(position) is True:
                self.winning_positions.append(position)
            self.all_positions.pop(0)
            self.broker.sell_position(position)
        self.total_trades += 1


    def check_if_position_wins(self, position):
        print(str(len(self.all_positions)))
        for item in self.all_positions:
            print(str(item.purchase_price))
            print(str(position.sell_price))
            if item.purchase_price < position.sell_price:
                return True

    def stop(self):
        balance = str(self.broker.get_balance())
        win_rate = str(self.calculate_win_rate())
        print("Final Balance: " + balance
              + " | Win Rate: " + win_rate
              + " | Total Trades: " + str(self.total_trades))
        self.print_winning_positions()

    def print_winning_positions(self):
        for position in self.winning_positions:
            print("Winning Positions Price: " + str(position.price))

    def calculate_win_rate(self):
        total_wins = len(self.winning_positions)
        total_positions = self.total_trades
        return total_wins/total_positions


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
    # Exit the position after an hour (sell out of the position) or 15 minutes after a downswing

    # 2. Bearish: When the MACD line crosses over to the negative side and is below the middle line, sell short to open the position after 15 minutes
    # Exit (buy to close) the position after an hour

    fifteen_minutes = 3
    one_hour = 12
    configuration = {   'enter_time': fifteen_minutes,
                        'exit_time': one_hour
                    }

    strategy.start(configuration)
    strategy.stop()

    # Winning Positions Price: 125.29
    # Winning Positions Price: 124.67
