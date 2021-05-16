from src.app.option_views import OptionViews
from src.app.td_authenticator import td_authenticator
import httpx

from tda.auth import easy_client
from tda.client import Client

from src.app import config


class App:

    views: OptionViews
    auth: td_authenticator

    def __init__(self):
        self.auth: td_authenticator = td_authenticator()
        self.views: OptionViews = OptionViews()

    def authenticate(self):
        self.auth.authenticate()

    def get_option_price_histoy(self, label: str):
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

    def plot_macd(self, label: str):
        self.views.get_macd(label)
        self.views.plot_macd_crossovers(label)

