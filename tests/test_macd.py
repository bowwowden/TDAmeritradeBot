import json

import pandas as pd
import pytest

from src.datainterface import ExampleData, DataSource
from src.indicators.macd import MACD

pd.set_option('display.max_rows', None)


@pytest.fixture
def DataFeed():
    example_data = ExampleData('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    dataframe = datasource.get_data()
    return dataframe


def test_macd_indicators_are_dataframe(DataFeed):
    macd = MACD()
    dataframe = macd.get_indicators(DataFeed)
    assert type(dataframe) == pd.DataFrame


# Correct Crossover Values For AAPL Pickle File
# Downswings = [ 126.1, 124.77, 125.02, 125.0503, 124.76, 124.61]
# Upswings = [ 125.58, 125.46, 125.1555, 124.9499, 124.6401]
def test_check_upswings(DataFeed):
    macd = MACD()

    dataframe = macd.get_crossover(dataframe=DataFeed)
    data = dataframe.to_json(orient='records')
    stock_data = json.loads(data)
    chkvalues = [ 125.58, 125.46, 125.1555, 124.9499, 124.6401]
    Upswings = []

    length = len(stock_data)
    for i in range(1, length):
        candlestick = stock_data[i]
        if candlestick['crossover'] == 'Upswing':
            Upswings.append(candlestick['close'])

    assert chkvalues == Upswings


def test_check_upswings_false(DataFeed):
    macd = MACD()

    dataframe = macd.get_crossover(dataframe=DataFeed)
    data = dataframe.to_json(orient='records')
    stock_data = json.loads(data)
    chkvalues = [125.58, 125.46, 1252000, 124.9499, 124.6401]
    Upswings = []

    length = len(stock_data)
    for i in range(1, length):
        candlestick = stock_data[i]
        if candlestick['crossover'] == 'Upswing':
            Upswings.append(candlestick['close'])

    assert chkvalues != Upswings


def test_check_downswings(DataFeed):
    macd = MACD()

    dataframe = macd.get_crossover(dataframe=DataFeed)
    data = dataframe.to_json(orient='records')
    stock_data = json.loads(data)

    chkvalues = [126.1, 124.77, 125.02, 125.0503, 124.76, 124.61]
    Downswings = []

    length = len(stock_data)
    for i in range(1, length):
        candlestick = stock_data[i]
        if candlestick['crossover'] == 'Downswing':
            Downswings.append(candlestick['close'])

    assert chkvalues == Downswings
