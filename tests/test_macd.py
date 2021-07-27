import pandas
import pytest

from src.datainterface import ExampleDataSource, DataSource
from src.indicators.macd import MACD
pandas.set_option('display.max_rows', None)

@pytest.fixture
def DataFeed():
    example_data = ExampleDataSource('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    return datasource.get_data()


def test_get_indicators(DataFeed):
    macd = MACD()
    macd.get_indicators(DataFeed)


def test_get_macd_swing_lines(DataFeed):
    macd = MACD()
    dataframe = macd.get_crossover(dataframe=DataFeed)
    print(dataframe)
    for candlestick in range(0, len(dataframe) - 1):
        if dataframe['Upswing_Signal_Price'][candlestick] > 0:
            print("Buy Price: ")
            UpSwingPrice = dataframe['close'][candlestick]
            print(UpSwingPrice)
        if dataframe['Downswing_Signal_Price'][candlestick] > 0:
            print("Sell Price: ")
            UpSwingPrice = dataframe['close'][candlestick]
            print(UpSwingPrice)


def test_get_macd_intersections(DataFeed):
    macd = MACD()
    intersections = macd.get_upswing_points(DataFeed)
    print(intersections)