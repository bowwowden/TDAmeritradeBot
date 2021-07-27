import numpy as np

from src.indicator import Indicator


class MACD(Indicator):

    def get_indicators(self, dataframe):
        dataframe = self.get_macd_indicators(dataframe)
        return dataframe

    def get_crossover(self, dataframe):
        dataframe = self.calculate_macd_signal_line_crossovers(dataframe)
        return dataframe

    def get_macd_indicators(self, dataframe):
        # Create new columns for the data
        indicators = self.calculate_macd_indicators(dataframe)
        dataframe['MACD'] = indicators[0]
        dataframe['Signal Line'] = indicators[1]
        return dataframe

    def calculate_macd_indicators(self, dataframe):
        ShortEMA = dataframe.close.ewm(span=12, adjust=False).mean()
        LongEMA = dataframe.close.ewm(span=26, adjust=False).mean()
        MovingAverageCD = ShortEMA - LongEMA
        signal = MovingAverageCD.ewm(span=9, adjust=False).mean()
        return [MovingAverageCD, signal]

    # Add labels to dataframe that are indicators of when the MACD and Signal Line crossover
    def calculate_macd_signal_line_crossovers(self, dataframe):
        dataframe = self.get_macd_indicators(dataframe)
        Upswing = []
        Downswing = []
        flag = -1
        for i in range(0, len(dataframe)):
            # Upswing
            if dataframe['MACD'][i] > dataframe['Signal Line'][i]:
                # haven't passed
                if flag != 1:
                    Upswing.append(dataframe['close'][i])
                    Downswing.append(np.nan)
                    flag = 1
                else:
                    Upswing.append(np.nan)
                    Downswing.append(np.nan)
            # Downswing
            elif dataframe['MACD'][i] < dataframe['Signal Line'][i]:
                if flag != 0:
                    Downswing.append(dataframe['close'][i])
                    Upswing.append(np.nan)
                    flag = 0
                else:
                    Downswing.append(np.nan)
                    Upswing.append(np.nan)
            else:
                Upswing.append(np.nan)
                Downswing.append(np.nan)

        dataframe['Upswing_Signal_Price'] = Upswing
        dataframe['Downswing_Signal_Price'] = Downswing
        return dataframe

    def get_upswing_points(self, dataframe) -> []:
        dataframe = self.get_macd_indicators(dataframe)
        upswing_ticks = []

        for i in range(1, len(dataframe)):
            if dataframe['MACD'][i] > dataframe['Signal Line'][i]:
                if dataframe['MACD'][i - 1] <= dataframe['Signal Line'][i - 1]:
                    upswing_ticks.append(dataframe['close'][i])
            else:
                upswing_ticks.append(np.nan)
        return upswing_ticks

    def get_downswing_points(self, dataframe) -> []:
        dataframe = self.get_macd_indicators(dataframe)
        downswing_ticks = []

        for i in range(1, len(dataframe)):
            if dataframe['MACD'][i] < dataframe['Signal Line'][i]:
                if dataframe['MACD'][i - 1] <= dataframe['Signal Line'][i - 1]:
                    downswing_ticks.append(dataframe['close'][i])
            else:
                downswing_ticks.append(np.nan)
        return downswing_ticks
