import pandas as pd

class Plot:

    def plot_stock_data(self, label: str, data):
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

    #
    # def plot_indicator(self):
    #     # Calculate and define moving average of 30 periods
    #     avg_30 = df.close.rolling(window=30, min_periods=1).mean()
    #
    #     # Calculate and define moving average of 50 periods
    #     avg_50 = df.close.rolling(window=50, min_periods=1).mean()
    #
    #     trace2 = {
    #         'x': xdt,
    #         'y': avg_30,
    #         'type': 'scatter',
    #         'mode': 'lines',
    #         'line': {
    #             'width': 1,
    #             'color': 'blue'
    #         },
    #         'name': 'Moving Average of 30 periods'
    #     }
    #
    #     trace3 = {
    #         'x': xdt,
    #         'y': avg_50,
    #         'type': 'scatter',
    #         'mode': 'lines',
    #         'line': {
    #             'width': 1,
    #             'color': 'red'
    #         },
    #         'name': 'Moving Average of 50 periods'
    #     }
    #
    #     data = [trace1, trace2, trace3]
    #     # Config graph layout
    #     layout = go.Layout({
    #         'title': {
    #             'text': label + 'Moving Average',
    #             'font': {
    #                 'size': 15
    #             }
    #         }
    #     })
    #
    #     fig = go.Figure(data=data, layout=layout)
    #     fig.write_html( label + "Moving Averages.html")
    #     fig.show()