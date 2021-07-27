import pytest

from src.datainterface import ExampleDataSource, DataSource
from src.indicators.macd import MACD
from src.minerva import Minerva
from src.strategy import Strategy


@pytest.fixture
def DataFeed():
    example_data = ExampleDataSource('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    return datasource


def test_minerva_load_example_data(DataFeed):
    minerva: Minerva = Minerva(DataFeed)
    example_data = minerva.load_data()
    assert example_data is not None


@pytest.fixture
def MACD_Strategy():
    macd = MACD()
    strategy = Strategy(macd)
    return strategy


# Implementation Test
def test_minerva_backtest_macd_signal_strategy(DataFeed, MACD_Strategy):
    minerva: Minerva = Minerva(DataFeed)
    minerva.set_strategy(MACD_Strategy)

    minerva.backtest_strategy()
    minerva.log_strategy_history()

    assert True


def test_minerva_backtest_without_strategy(DataFeed):
    minerva: Minerva = Minerva(DataFeed)
    minerva.backtest_strategy()

    assert True


def test_minerva_backtest_with_one_strategy():
    minerva: Minerva = Minerva()
    strategy: Strategy = Strategy()
    minerva.add_strategy(strategy)
    minerva.backtest()
    assert False