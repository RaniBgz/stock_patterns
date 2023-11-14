'''
The Frame class describes the data obtained when performing one query on a stock from start_time to end_time
It holds basic information that allows to find the data and reason with it.
It also holds a list of patterns
'''

import math
from typing import List
from BoundingBox2D import BoundingBox2D
from Pattern import Pattern


class Frame:

    def __init__(self, stock_name, interval, start_time, end_time, candles, nb_candles, csv_path, img_path, res_width, res_height, patterns):
        self.stock_name = stock_name
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.candles = candles
        self.nb_candles = nb_candles
        self.csv_path = csv_path
        self.img_path = img_path
        self.img_res = (res_width, res_height)
        self.patterns = patterns


    def __str__(self) -> str:
        return f'Frame for {self.stock_name} stock and {self.interval} starts at {self.start_time} and ends at {self.end_time}\n' \
               f'It contains {self.nb_candles} Candles and {len(self.patterns)} Patterns'

    #Used to convert a list of BoundingBox2D passed as parameters into a list of Patterns that will be attributed to the current frame
    def convert_bb2d_to_patterns(self, bounding_boxes: List[BoundingBox2D]):
        print(f'Current frame has: {self.nb_candles} candles')
        candle_width = self.img_res[0]/self.nb_candles
        for bbox in bounding_boxes:
            bbox.compute_corners_from_center_and_WH()
            #Computing absolute x coordinate of the bottom left and bottom right corners of the bounding box
            x1 = bbox.corners[0][0]*self.img_res[0]
            x2 = bbox.corners[-1][0]*self.img_res[0]
            #TODO: add check for min-max cases
            #Computing first and last candle of the pattern, extracting pattern candle list
            first_candle = math.floor(x1/candle_width)
            last_candle = math.ceil(x2/candle_width)
            pattern_candles = self.candles[first_candle:last_candle]
            print(f"Pattern starts at candle {first_candle} and ends at candle {last_candle}")
            # name, confidence, start_time, end_time, candles)
            #TODO: Fix confidence and end time, current end-time is one-candle duration short. will need to add duration to candle or add some interval conversion
            #Patterns may be shifted by one candle
            pattern = Pattern(bbox.name, 0, self.candles[first_candle].start_time, self.candles[last_candle].start_time, pattern_candles)
            print(pattern.__str__())
            self.patterns.append(pattern)


