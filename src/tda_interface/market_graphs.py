import pandas as pd
import plotly.graph_objects as go
from matplotlib import pyplot as plt

from src.technical_analysis import technical_analysis


class market_graphs:

    market_analyzer: technical_analysis = technical_analysis()

    def plot_moving_averages(self, label: str, data):
        # retrieve actual price history data
        ticker_data = data['candles']

        # create a pandas DataFrame with candles
        df = pd.DataFrame(ticker_data)

        xdt = pd.to_datetime(df.datetime, unit='ms')
        trace1 = {
            'x': xdt,
            'open': df.open,
            'close': df.close,
            'high': df.high,
            'low': df.low,
            'type': 'candlestick',
            'name': 'SPX',
            'showlegend': False
        }

        # Calculate and define moving average of 30 periods
        avg_30 = df.close.rolling(window=30, min_periods=1).mean()

        # Calculate and define moving average of 50 periods
        avg_50 = df.close.rolling(window=50, min_periods=1).mean()

        trace2 = {
            'x': xdt,
            'y': avg_30,
            'type': 'scatter',
            'mode': 'lines',
            'line': {
                'width': 1,
                'color': 'blue'
            },
            'name': 'Moving Average of 30 periods'
        }

        trace3 = {
            'x': xdt,
            'y': avg_50,
            'type': 'scatter',
            'mode': 'lines',
            'line': {
                'width': 1,
                'color': 'red'
            },
            'name': 'Moving Average of 50 periods'
        }

        data = [trace1, trace2, trace3]
        # Config graph layout
        layout = go.Layout({
            'title': {
                'text': label + 'Moving Average',
                'font': {
                    'size': 15
                }
            }
        })

        fig = go.Figure(data=data, layout=layout)
        fig.write_html( label + "Moving Averages.html")
        fig.show()

    def plot_macd_buy_sell(self, label: str, data):
        signal_line = self.market_analyzer.get_signal_line(data)

    def plot_data(self, MACD_Dataframe):
        # Show the data
        plt.figure(figsize=(12.2, 4.5))
        plt.scatter(MACD_Dataframe.index, MACD_Dataframe['Buy_Signal_Price'], color='green', label='Buy',
                    marker='^', alpha=1)
        plt.scatter(MACD_Dataframe.index, MACD_Dataframe['Sell_Signal_Price'], color='red', label='Sell',
                    marker='v', alpha=1)
        plt.plot(MACD_Dataframe['close'], label='Close Price', alpha=0.35)
        plt.title('Close Price Buy and Sell Signals')
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Close Price USD ($)')
        plt.legend(loc='upper left')
        plt.show()



