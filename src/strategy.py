from src.indicator import Indicator


class StrategyInterface:
    def __init__(self):
        pass

    def next(self, ticker):
        pass

    def run_strategy(self, dataframe):
        pass

    def get_positions(self, dataframe):
        pass

    def backtest(self, dataframe):
        pass


class Strategy(StrategyInterface):
    _indicator = None
    positions = list()

    def __init__(self, indicator: Indicator):
        super().__init__()
        self._indicator = indicator

    def backtest(self, dataframe):
        _positions = list()
        _dataframe = self._indicator.get_crossover(dataframe)

        for candlestick in range(0, len(_dataframe) - 1):

            option_purchase_price = self.buy_calls_after_15_minutes(_dataframe, candlestick)

            if option_purchase_price is not None:
                buy_or_sell = 'Buy'
                position = [option_purchase_price, buy_or_sell]
                _positions.append(position)

            option_sell_price = self.buy_puts_after_15_minutes(_dataframe, candlestick)
            if option_sell_price is not None:
                buy_or_sell = 'Sell'
                position = [option_sell_price, buy_or_sell]
                _positions.append(position)

        self.set_positions(_positions)

    def set_positions(self, list):
        self.positions = list

    def get_positions(self):
        return self.positions

    def next(self, ticker):
        pass

    def buy_calls_after_15_minutes(self, dataframe, candlestick):
        if dataframe['Upswing_Signal_Price'][candlestick] > 0:
            print("Buy Price")
            print(dataframe['Upswing_Signal_Price'][candlestick])
            try:
                if dataframe['MACD'][candlestick + 2] > dataframe['Signal Line'][candlestick + 2]:
                    buy_price_after_15_minutes = dataframe['close'][candlestick + 2]
                    return buy_price_after_15_minutes
            except IndexError:
                print("index error at " + str(candlestick))
            return None

    def buy_puts_after_15_minutes(self, dataframe, candlestick):
        if dataframe['Downswing_Signal_Price'][candlestick] > 0:
            print("Sell Price:")
            print(dataframe['Downswing_Signal_Price'][candlestick])
            try:
                if dataframe['MACD'][candlestick + 2] < dataframe['Signal Line'][candlestick + 2]:
                    sell_price_after_15_minutes = dataframe['close'][candlestick + 2]
                    return sell_price_after_15_minutes
            except IndexError:
                print("index error at " + str(candlestick))
            return None
