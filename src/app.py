import httpx
from tda.auth import easy_client
from tda.client import Client

from src.model import config
from src.model.market_graphs import market_graphs
from src.model.td_authenticator import td_authenticator


class App:

    graphs: market_graphs
    auth: td_authenticator

    def __init__(self):
        self.auth: td_authenticator = td_authenticator()
        self.graphs: market_graphs = market_graphs()

    def authenticate(self):
        self.auth.authenticate()

    def plot_moving_averages(self, label: str):
        data = self.get_stock_price_histoy(label)
        self.graphs.plot_moving_averages(label, data)

    @staticmethod
    def get_stock_price_histoy(label: str):
        c = easy_client(
            api_key=config.API_KEY,
            redirect_uri=config.REDIRECT_URI,
            token_path=config.TOKEN_PATH)

        # get price in 5 minute candles
        resp = c.get_price_history(label,
                                   period_type=Client.PriceHistory.PeriodType.DAY,
                                   period=Client.PriceHistory.Period.ONE_DAY,
                                   frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                                   frequency=Client.PriceHistory.Frequency.EVERY_FIVE_MINUTES)
        assert resp.status_code == httpx.codes.OK
        history = resp.json()
        return history

    def get_option_chain(self, label: str):
        c = easy_client(
            api_key=config.API_KEY,
            redirect_uri=config.REDIRECT_URI,
            token_path=config.TOKEN_PATH)
        resp = c.get_option_chain()
