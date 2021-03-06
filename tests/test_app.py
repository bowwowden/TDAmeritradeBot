import pytest

from src.app import App


@pytest.fixture
def app():
    app: App = App()
    return app


def test_app_authentication(app):
    app.authenticate()
    assert True


def test_get_stock_history(app, label: str = 'AAPL'):
    data: str = app.get_stock_price_histoy(label)
    print(data)
    assert True


def test_plot_macd_crossovers(app, label: str = 'AAPL'):
    app.plot_moving_averages(label)
    assert True