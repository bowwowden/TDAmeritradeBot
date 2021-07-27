import pandas as pd


# Interface
class DataInterface:
    def __init__(self):
        pass

    def get_data(self):
        pass


# Adapter
class DataSource(DataInterface):
    _datafeed = None

    def __init__(self, datafeed):
        super().__init__()
        self._datafeed = datafeed

    def get_data(self):
        return self._datafeed.load_data()

    def get_data_as_list(self):
        return self._datafeed.tolist()


class ExampleDataSource:
    ticker_data: pd = None
    file_location: str = None

    def __init__(self, file_location: str):
        self.file_location = file_location
        self.ticker_data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        self.ticker_data = pd.read_pickle(self.file_location)
        ticker_dataframe = pd.DataFrame(data=self.ticker_data)
        ticker_dataframe = ticker_dataframe.set_index(
            pd.to_datetime(ticker_dataframe['datetime'], unit='ms'))
        return ticker_dataframe
