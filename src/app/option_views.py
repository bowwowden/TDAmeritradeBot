import matplotlib.pyplot as plt
import pyEX as p


class OptionViews:

    def get_macd(self, label: str):
        ticker = label
        timeframe = '5m'
        df = p.chartDF(ticker, timeframe, token="sk_335abdd65af64ef49f15e8ccef80bc84")
        df = df[['close']]
        df.reset_index(level=0, inplace=True)
        df.columns = ['ds', 'y']
        plt.plot(df.ds, df.y, label=label)

    def plot_macd_crossovers(self, label: str):
        plt.rcParams['figure.figsize'] = (15, 5)
        ticker = label
        timeframe = '5m'
        df = p.chartDF(ticker, timeframe, token="sk_335abdd65af64ef49f15e8ccef80bc84")
        df = df[['close']]
        df.reset_index(level=0, inplace=True)
        df.columns = ['ds', 'y']
        exp1 = df.y.ewm(span=12, adjust=False).mean()
        exp2 = df.y.ewm(span=26, adjust=False).mean()

        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
        plt.plot(df.ds, macd, label=label + ' MACD', color='#EBD2BE')
        plt.plot(df.ds, exp3, label='Signal Line', color='#E5A4CB')
        plt.legend(loc='upper left')
        plt.show()
