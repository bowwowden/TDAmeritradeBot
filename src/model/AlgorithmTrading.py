import numpy as np
from matplotlib import pyplot as plt

from src.controller.app import App

app: App = App()

app.authenticate()

apple_data = app.get_option_price_histoy('SPY')
ticker_data = apple_data['candles']

import pandas as pd

df = pd.DataFrame(data=ticker_data)


# # set date to be index
# xdt = pd.to_datetime(df.datetime, unit='ms')
df = df.set_index(pd.to_datetime(df['datetime'], unit='ms'))
# show the data
print(df)
# # visually show stock price
# plt.figure(figsize=(12.2, 4.5))
# plt.plot(df['close'], label = 'close')
# plt.xticks(rotation=45)
# plt.title('Close Price History')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.show()

# Calculate the MACF and signal line indicators
# Calculate the short term exponential moving average (EMA) for 12 periods
ShortEMA = df.close.ewm(span=12, adjust=False).mean()
# Calculate the long term exponential moving average (EMA)
LongEMA = df.close.ewm(span=26, adjust=False).mean()
# Calculate the MACD Line
MACD = ShortEMA - LongEMA
# Calculate the signal line
signal = MACD.ewm(span=9, adjust=False).mean()

# Plot chart
# The Zero is the Middle Line
plt.figure(figsize=(12.2, 4.5))
plt.plot(df.index, MACD, label='AAPL MACD', color='red')
plt.plot(df.index, signal, label='Signal Line', color='blue')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()

# Create new columns for the data
df['MACD'] = MACD
df['Signal Line'] = signal
# Show the data
print(df)


# Create a function when to buy and sell an asset
def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        # if macd is greater than signal
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            # then flag hasn't been set before
            if flag != 1:
                Buy.append(signal['close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        # signal line has crossed macd
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            # then flag hasn't been setefore
            if flag != 0:
                Sell.append(signal['close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return (Buy, Sell)


# Create a buy and sell column
a = buy_sell(df)
df['Buy_Signal_Price'] = a[0]
df['Sell_Signal_Price'] = a[1]

# Show the data
print(df)
# plt.figure(figsize=(12.2, 4.5))
# plt.scatter(df.index, df['Buy_Signal_Price'], color='green', label='Buy', marker='^', alpha=1)
# plt.scatter(df.index, df['Sell_Signal_Price'], color='red', label='Sell', marker='v', alpha=1)
# plt.plot(df['close'], label='Close Price', alpha=0.35)
# plt.title('Close Price Buy and Sell Signals')
# plt.xticks(rotation=45)
# plt.xlabel('Date')
# plt.ylabel('Close Price USD ($)')
# plt.legend(loc = 'upper left')
# plt.show()