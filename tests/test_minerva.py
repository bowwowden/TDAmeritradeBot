import pytest

from src.datainterface import ExampleData, DataSource, DataInterface
from src.minerva import Minerva


@pytest.fixture
def DataFeed():
    example_data = ExampleData('example_data/AAPL61Data')
    datasource: DataInterface = DataSource(example_data)
    return datasource


def test_minerva_load_example_data(DataFeed):
    minerva: Minerva = Minerva(DataFeed)
    example_data = minerva.load_data()
    print(type(example_data))
    assert example_data is not None


@pytest.fixture
def macd_strategy_conf():
    fifteen_minutes = 3
    one_hour = 12
    configuration = {'name': 'MACD_Strategy',
                     'enter_behavior': 'Upswing',
                     'enter_time': fifteen_minutes,
                     'exit_behavior': 'Downswing',
                     'exit_time': one_hour,
                     'quantity': 1,
                     'log': True
                     }
    return configuration


# Implementation Test
def test_minerva_add_strategy(DataFeed, macd_strategy_conf):
    minerva: Minerva = Minerva(DataFeed)
    minerva.add_strategy(macd_strategy_conf)

    assert len(minerva.get_strategies()) > 0


def test_run_test_single_macd_strategy(DataFeed, macd_strategy_conf):
    # Brokerage automatically uses 10000 in starting cash
    # Add the signal parameters to the strategy using preconfigured options
    # 1. Bullish: When the MACD line crosses over to the positive side and is above the middle line, buy into the stock after 15 minutes.
    # Exit the position after an hour (sell out of the position) or 15 minutes after a downswing
    # 2. Bearish: When the MACD line crosses over to the negative side and is below the middle line, sell short to open the position after 15 minutes
    # Exit (buy to close) the position after an hour
    minerva: Minerva = Minerva(DataFeed)

    minerva.backtest_strategy(macd_strategy_conf)

    minerva.start()
    minerva.stop()
    minerva.print_trade_history()

    chk_positions: list = [{'purchase': 125.5, 'sell': 125.09},
                           {'purchase': 125.39, 'sell': 124.9966},
                           {'purchase': 125.195, 'sell': 125.29},
                           {'purchase': 125.075, 'sell': 125.0555},
                           {'purchase': 124.59, 'sell': 124.67}]

    trade_history = minerva.get_strategy_trade_history(name='MACD_Strategy')
    assert trade_history == chk_positions
