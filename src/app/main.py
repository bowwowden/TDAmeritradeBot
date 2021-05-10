import datetime
import json

import httpx
from tda import auth, client
from tda.auth import easy_client
from tda.client import Client

from src.app import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# macd imports
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pyEX as p
from iexfinance.refdata import get_symbols


class app_authenticator:
    def __init__(self):
        pass

    @staticmethod
    def authenticate():
        try:
            c = auth.client_from_token_file(config.TOKEN_PATH, config.API_KEY)
        except FileNotFoundError:
            with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                c = auth.client_from_login_flow(
                    driver, config.API_KEY, config.REDIRECT_URI, config.TOKEN_PATH)


class stream_option_data:
    def __init__(self):
        pass

    def get_label_price_histoy(self, LABEL: str):
        c = easy_client(
            api_key=config.API_KEY,
            redirect_uri=config.REDIRECT_URI,
            token_path=config.TOKEN_PATH)

        resp = c.get_price_history(LABEL,
                                   period_type=Client.PriceHistory.PeriodType.DAY,
                                   period=Client.PriceHistory.Period.ONE_DAY,
                                   frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                                   frequency=Client.PriceHistory.Frequency.EVERY_FIVE_MINUTES)
        assert resp.status_code == httpx.codes.OK
        history = resp.json()
        return history


class option_strategy_executor:

    def __init__(self):
        pass

    def get_macd(self, label: str):
        ticker = label
        timeframe = '6m'
        df = p.chartDF(ticker, timeframe, token="sk_335abdd65af64ef49f15e8ccef80bc84")
        df = df[['close']]
        df.reset_index(level=0, inplace=True)
        df.columns = ['ds', 'y']
        plt.plot(df.ds, df.y, label=label)
        plt.show()


class analysis_genesis:
    def __init__(self):
        pass

    # set chart to 5 minute candles
