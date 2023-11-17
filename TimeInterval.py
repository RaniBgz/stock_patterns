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
