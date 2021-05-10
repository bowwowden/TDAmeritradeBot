import pytest

from src.app.main import app_authenticator, stream_option_data, option_strategy_executor, analysis_genesis


@pytest.fixture
def setUp_App():
    app: app_authenticator = app_authenticator()
    return app


def test_authenticate(setUp_App):
    # authenticate
    setUp_App.authenticate()
    assert True


def test_stream_data(setUp_App):
    # stream data
    order_maker: stream_option_data = stream_option_data()
    # get price history for AAPL
    print(str(order_maker.get_label_price_histoy('AAPL')))
    assert True


def test_analyze_json():
    analyzer: analysis_genesis = analysis_genesis()


def test_get_macd_index():
    # option bot
    option_bot: option_strategy_executor = option_strategy_executor()
    option_bot.get_macd('AAPL')
    pass




