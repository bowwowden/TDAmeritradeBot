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
