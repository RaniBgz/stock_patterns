'''
The Frame class describes the data obtained when performing one query on a stock from start_time to end_time
It holds basic information that allows to find the data and reason with it.
It also holds a list of patterns
'''


class Frame:

    def __init__(self, stock_name, interval, start_time, end_time, candles, nb_candles, csv_path, img_path, patterns):
        self.stock_name = stock_name
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.candles = candles
        self.nb_candles = nb_candles
        self.csv_path = csv_path
        self.img_path = img_path
        self.patterns = patterns


    def __str__(self) -> str:
        return f'Frame for {self.stock_name} stock and {self.interval} starts at {self.start_time} and ends at {self.end_time}\n' \
               f'It contains {self.nb_candles} Candles and {len(self.patterns)} Patterns'