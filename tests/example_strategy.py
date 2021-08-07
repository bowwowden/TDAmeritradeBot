import json

import pandas as pd

from src.paperbroker import Broker
from src.indicator import Indicator
from src.position import Position
from src.strategy import Strategy


class TestStrategy(Strategy):
    broker = Broker()
    indicators = list()
    winning_positions = list()
    all_positions = list()
    total_trades: int = 0

    def __init__(self, data: pd):
        super().__init__()
        self.data = data
        self.broker.set_starting_cash(10000)

    def print_stock_data(self):
        data = self.get_dataframe_as_json(self.data)
        for candlestick in data:
            print(candlestick)

    def add_indicator(self, indicator: Indicator):
        data = indicator.get_crossover(self.data)
        indicator.data = self.get_dataframe_as_json(data)
        self.indicators.append(indicator)

    def get_dataframe_as_json(self, data: pd):
        data = data.to_json(orient='records')
        data = json.loads(data)
        return data

    def get_indicators(self) -> list:
        return self.indicators

    def start(self, configuration):
        stock_data = self.get_dataframe_as_json(self.data)

        enter_time: int = configuration['enter_time']
        exit_time: int = configuration['exit_time']
        quantity: int = configuration['quantity']

        buy_position_index = 0
        exit_position_index = 0
        sell_position_index = 0

        length = len(stock_data)
        for i in range(0, length):

            position: Position = Position()
            candlestick = stock_data[i]
            price: int = candlestick['close']

            # Buy Flag
            if candlestick['crossover'] == 'Upswing':
                # 15 minutes later
                buy_position_index = i + enter_time
                # 1 hour later
                exit_position_index = buy_position_index + exit_time

            # Buy After 15 Minutes
            if i == buy_position_index and i != 0:
                position.set_quantity(quantity)
                position.set_price(price)
                position.set_purchase_price(price)
                self.enter_position(position)

            # Sell Flag
            if candlestick['crossover'] == 'Downswing':
                # sell after 5 minutes
                sell_position_index = i + 3

            # If 15 minutes after downswing or 1 hour entering position, or last tick
            if ((i == sell_position_index or i == exit_position_index) and self.broker.has_position()) or i == length:
                position.set_quantity(quantity)
                position.set_price(price)
                position.set_sell_price(price)
                self.exit_position(position)

            if configuration['log'] is True:
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
        price = position.price
        if self.broker.has_position():
            if self.check_if_position_wins(position) is True:
                self.winning_positions.append(position)
            self.broker.sell_position(position)
            self.set_sell_price_most_recent_position(price)
        self.total_trades += 1

    def set_sell_price_most_recent_position(self, price):
        position: Position = self.all_positions[-1]
        position.set_sell_price(price)

    def check_if_position_wins(self, position):
        last_position = self.all_positions[-1]
        if position.sell_price > last_position.purchase_price:
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
            print("Winning Positions Price: " + str(position.price)
                  + " Sell Price: " + str(position.sell_price))

    def print_trade_history(self):
        print("Printing the Trade History")
        for position in self.all_positions:
            print("Position Purchase Price: " + str(position.price)
                  + " Sell Price: " + str(position.sell_price))

    def calculate_win_rate(self):
        total_wins = len(self.winning_positions)
        total_positions = self.total_trades
        return total_wins / total_positions

    def get_all_positions(self):
        return self.all_positions

    def get_all_positions_price_as_list(self):
        position_prices: list = []
        for position in self.all_positions:
            position_prices.append({'purchase': position.purchase_price, 'sell': position.sell_price})
        return position_prices