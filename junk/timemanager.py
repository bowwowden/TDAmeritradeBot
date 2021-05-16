import datetime


class TimeManager:

    # Mountain Standard Time Regular Trading Hours: 7:30 AM - 2:00 PM
    # Pacific Standard Time Regular Trading Hours: 6:30 AM - 1:00 PM
    # NYSE UTC Trading Hours: 14:30 - 21:00

    start_time: int
    end_time: int

    def __init__(self):
        # Set Time Zone to Arizona Mountain Time
        pass

    def convert_candlestick_time(self, time_in_utc: int)->datetime:
        converted_time: datetime = datetime.datetime.fromtimestamp(time_in_utc / 1000)
        return converted_time

    def calculate_wait_time(self, current_time: int)->int:
        minute_milliseconds: int = 60000
        fifteen_minutes: int = 15 * minute_milliseconds
        return current_time + fifteen_minutes