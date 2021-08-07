import abc

import pandas as pd


class Strategy(abc.ABC):
    _indicator = None
    positions = list()
    data: pd

    def __init__(self):
        pass

    @abc.abstractmethod
    def start(self, configuration):
        pass

