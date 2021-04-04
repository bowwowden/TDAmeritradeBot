import datetime

import pandas_datareader as web


class main:
    tda_apikey = "DRBKZQKGIVCYUYD83VGHXDMUVKKX3TDR"

    def __init__(self):
        pass

    def auth(self):
        pass

    # requests require user and apikey authorization

    def display_market_data(self):
        start = datetime.datetime(2019, 1, 1)
        end = datetime.datetime(2019, 1, 10)
        facebook = web.DataReader("FB", 'morningstar', start, end)
        print(facebook.head())
