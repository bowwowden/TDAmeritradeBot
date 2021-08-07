import pytest

from src.datainterface import ExampleData, DataSource
from tests.example_strategy import TestStrategy
from src.indicators.macd import MACD


@pytest.fixture
def DataFeed():
    example_data = ExampleData('example_data/AAPL61Data')
    datasource = DataSource(example_data)
    dataframe = datasource.get_data()
    return dataframe


def test_strategy_print_stock_data(DataFeed):
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    strategy.print_stock_data()
    assert True


def test_strategy_indicator_to_json(DataFeed):
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    assert type(strategy.get_dataframe_as_json(data=DataFeed)) is list


def test_strategy_add_indicator(DataFeed):
    macd: MACD = MACD()
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    strategy.add_indicator(macd)
    print("Indicator Data\n")
    print(strategy.get_indicators()[0].data)
    assert len(strategy.get_indicators()) > 0


@pytest.fixture
def StrategyMacd(DataFeed):
    macd: MACD = MACD()
    strategy: TestStrategy = TestStrategy(data=DataFeed)
    strategy.add_indicator(macd)
    return strategy


def test_trade_history_is_correct(DataFeed):
    macd: MACD = MACD()
    dataframe = macd.get_crossover(DataFeed)
    strategy: TestStrategy = TestStrategy(data=dataframe)

    fifteen_minutes = 3
    one_hour = 12
    quantity = 1
    configuration = {'enter_time': fifteen_minutes,
                     'exit_time': one_hour,
                     'quantity': quantity,
                     'log': False,
                     }

    strategy.start(configuration)
    strategy.stop()
    strategy.print_trade_history()

    chk_positions: list = [{'purchase': 125.5, 'sell': 125.09},
                           {'purchase': 125.39, 'sell': 124.9966},
                           {'purchase': 125.195, 'sell': 125.29},
                           {'purchase': 125.075, 'sell': 125.0555},
                           {'purchase': 124.59, 'sell': 124.67}]

    trade_history = strategy.get_all_positions_price_as_list()
    assert trade_history == chk_positions


@pytest.mark.skip()
def test_macd_bullish_bearish_strategy(DataFeed):
    macd: MACD = MACD()
    dataframe = macd.get_crossover(DataFeed)
    strategy: TestStrategy = TestStrategy(data=dataframe)

    # Brokerage automatically uses 10000 in starting cash
    # Add the signal parameters to the strategy using preconfigured options

    # 1. Bullish: When the MACD line crosses over to the positive side and is above the middle line, buy into the stock after 15 minutes.
    # Exit the position after an hour (sell out of the position) or 15 minutes after a downswing

    # 2. Bearish: When the MACD line crosses over to the negative side and is below the middle line, sell short to open the position after 15 minutes
    # Exit (buy to close) the position after an hour

    fifteen_minutes = 3
    one_hour = 12
    configuration = {'enter_time': fifteen_minutes,
                     'exit_time': one_hour,
                     'log': True
                     }

    strategy.start(configuration)
    strategy.stop()
    strategy.print_trade_history()

    # Winning Positions Price: 125.29
    # Winning Positions Price: 124.67
    assert False
