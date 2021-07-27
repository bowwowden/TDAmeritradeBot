import abc


class BrokerageAPI(abc.ABC):

    @abc.abstractmethod
    def authenticate(self):
        pass

