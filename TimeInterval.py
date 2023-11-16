class TimeInterval:
    _durations = {
        "1m": 1,
        "2m": 2,
        "5m": 5,
        "15m": 15,
        "1h": 60,
        "1d": 1440,
        "1wk": 10080,
        "1mo": 43800,  # Approximation
        "3mo": 131400,  # Approximation
    }

    def __init__(self, interval):
        self.interval = interval
        self.minutes = self._durations[interval]

    def __str__(self):
        return f"{self.interval} ({self.minutes} minutes)"

    def __lt__(self, other):
        return self.minutes < other.minutes

    def __le__(self, other):
        return self.minutes <= other.minutes

    def __eq__(self, other):
        return self.minutes == other.minutes

    def __ne__(self, other):
        return self.minutes != other.minutes

    def __gt__(self, other):
        return self.minutes > other.minutes

    def __ge__(self, other):
        return self.minutes >= other.minutes

    @classmethod
    def from_minutes(cls, minutes):
        for interval, mins in cls._durations.items():
            if mins == minutes:
                return cls(interval)
        raise ValueError("No interval corresponds to the given duration in minutes.")
#
# # Usage
# one_hour = TimeInterval("1h")
# one_day = TimeInterval("1d")
#
# print(one_hour)  # Output: 1h (60 minutes)
# print(one_day)  # Output: 1d (1440 minutes)
#
# print(one_hour < one_day)  # Output: True
#
# # Convert from minutes to interval string
# thirty_minutes = TimeInterval.from_minutes(30)
# print(thirty_minutes)  # Output: 30m (30 minutes)


# from enum import Enum
#
# class TimeInterval(Enum):
#     MINUTE = 1
#     HOUR = 60
#     DAY = 1440
#     WEEK = 10080
#     MONTH = 43800  # Approximation, as a month can vary in duration
#
#     # Associate strings with durations
#     durations = {
#         "1m": MINUTE,
#         "2m": MINUTE * 2,
#         "5m": MINUTE * 5,
#         "15m": MINUTE * 15,
#         "1h": HOUR,
#         "1d": DAY,
#         "1wk": WEEK,
#         "1mo": MONTH,
#         "3mo": MONTH * 3,
#     }
#
#     @classmethod
#     def get_duration(cls, interval_string):
#         return cls.durations[interval_string].value
#
#     @classmethod
#     def compare_intervals(cls, interval1, interval2):
#         return cls.get_duration(interval1) - cls.get_duration(interval2)
#
# # Usage
# print(TimeInterval.get_duration("1h"))  # Output: 60
# print(TimeInterval.compare_intervals("1h", "1d"))  # Output: -1380