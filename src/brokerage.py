import abc


class BrokerageAPI(abc.ABC):

    @abc.abstractmethod
    def authenticate(self):
        pass

    @abc.abstractmethod
    def get_stock_price_history(self, label, order_params):
        pass

