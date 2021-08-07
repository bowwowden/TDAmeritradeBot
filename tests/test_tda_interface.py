import pytest

from src.brokerage import BrokerageAPI
from src.tda_interface.tda_interface import Tda_Interface


@pytest.fixture
def tda_api_client():
    tda_api_client: BrokerageAPI = Tda_Interface()
    return tda_api_client


def test_authenticate(tda_api_client):
    tda_api_client.authenticate()
    assert True


# @pytest.fixture
# def stock_query_params():
#     stock_query_params = {period_type:}
#     return stock_query_params
#
#
# def test_get_stock_price_histoy(tda_api_client, stock_query_params):
#     label = stock_query_params.label
#     resp = tda_api_client.get_stock_price_history(label, stock_query_params)
#     print(resp)