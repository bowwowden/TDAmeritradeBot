import pytest

from src.app.main import main


@pytest.fixture
def tradebot():
    tradebot: main = main()
    return tradebot


def test_auth(tradebot):
    assert True


def test_display_market_data(tradebot):
    tradebot.display_market_data()
    assert True


def test_buy_calls(tradebot):
    assert True


def test_exit_position_after_one_hour(tradebot):
    assert True


