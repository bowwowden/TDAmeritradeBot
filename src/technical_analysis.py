import numpy as np
import pandas as pd


class technical_analysis:

    def get_signal_line(self, data):
        ticker_data = data['candles']
        df = pd.DataFrame(data=ticker_data)
        df = df.set_index(pd.to_datetime(df['datetime'], unit='ms'))
        # Calculate the MACF and signal line indicators
        # Calculate the short term exponential moving average (EMA) for 12 periods
        ShortEMA = df.close.ewm(span=12, adjust=False).mean()
        # Calculate the long term exponential moving average (EMA)
        LongEMA = df.close.ewm(span=26, adjust=False).mean()
        # Calculate the MACD Line
        MACD = ShortEMA - LongEMA
        # Calculate the signal line
        signal = MACD.ewm(span=9, adjust=False).mean()
        return signal

    def set_indicators(self, dataframe):
        # Create new columns for the data
        indicators = self.calculate_macd_indicators()
        dataframe['MACD'] = indicators[0]
        dataframe['Signal Line'] = indicators[1]

        # Create a buy and sell column
        buy_sell_signals = self.buy_sell(dataframe)
        dataframe['Buy_Signal_Price'] = buy_sell_signals[0]
        dataframe['Sell_Signal_Price'] = buy_sell_signals[1]

    def calculate_macd_indicators(self, dataframe):
        # Calculate the short term exponential moving average (EMA) for 12 periods
        ShortEMA = dataframe.close.ewm(span=12, adjust=False).mean()
        # Calculate the long term exponential moving average (EMA)
        LongEMA = dataframe.close.ewm(span=26, adjust=False).mean()
        # Calculate the MACD Line
        MACD = ShortEMA - LongEMA
        # Calculate the signal line
        signal = MACD.ewm(span=9, adjust=False).mean()
        return [MACD, signal]

    # Create a function when to buy and sell an asset
    def buy_sell(self, data_frame):
        Buy = []
        Sell = []
        flag = -1

        for i in range(0, len(data_frame)):
            # if macd is greater than signal
            if data_frame['MACD'][i] > data_frame['Signal Line'][i]:
                Sell.append(np.nan)
                # then flag hasn't been set before
                if flag != 1:
                    Buy.append(data_frame['close'][i])
                    flag = 1
                else:
                    Buy.append(np.nan)
            # signal line has crossed macd
            elif data_frame['MACD'][i] < data_frame['Signal Line'][i]:
                Buy.append(np.nan)
                # then flag hasn't been set before
                if flag != 0:
                    Sell.append(data_frame['close'][i])
                    flag = 0
                else:
                    Sell.append(np.nan)
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        return (Buy, Sell)
