'''
This class defines a OHLC Candle (+start_time and volume)
'''

class Candle:
    def __init__(self, start_time, open, high, low, close, volume):
        self.start_time = start_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

