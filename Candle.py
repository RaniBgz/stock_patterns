'''
This class defines a OHLC Candle (+volume)
'''


class Candle:
    def __int__(self, open, high, low, close, volume):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

