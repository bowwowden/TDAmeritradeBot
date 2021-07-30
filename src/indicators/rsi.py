from src.indicator import Indicator


class RelativeStrengthIndex(Indicator):
    '''Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    It measures momentum by calculating the ration of higher closes and
    lower closes after having been smoothed by an average, normalizing
    the result between 0 and 100

    Formula:
      - up = upday(data)
      - down = downday(data)
      - maup = movingaverage(up, period)
      - madown = movingaverage(down, period)
      - rs = maup / madown
      - rsi = 100 - 100 / (1 + rs)

    The moving average used is the one originally defined by Wilder,
    the SmoothedMovingAverage

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index

    Notes:
      - ``safediv`` (default: False) If this parameter is True the division
        rs = maup / madown will be checked for the special cases in which a
        ``0 / 0`` or ``x / 0`` division will happen

      - ``safehigh`` (default: 100.0) will be used as RSI value for the
        ``x / 0`` case

      - ``safelow``  (default: 50.0) will be used as RSI value for the
        ``0 / 0`` case
    '''

    def __init__(self):
        upday = None
        downday = None
        maup = None
        madown = None

    # def _rscalc(self, rsi):
    #     try:
    #         rs = (-100.0 / (rsi - 100.0)) - 1.0
    #     except ZeroDivisionError:
    #         return float('inf')
    #
    #     return rs