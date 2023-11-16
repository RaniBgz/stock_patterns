'''
This class defines a OHLC Candle (+start_time and volume)
'''
from TimeInterval import TimeInterval


class Candle:
    def __init__(self, start_time, interval, open, high, low, close, volume):
        #TODO: add duration
        self.start_time = start_time
        self.interval = TimeInterval(interval)
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

