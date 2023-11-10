'''
A Pattern describes the information of any pattern found inside a data frame after running a Yolo detection on the image
'''


class Pattern:

    def __init__(self, name, confidence, start_time, end_time, candles):
        self.name = name
        self.confidence = confidence
        self.start_time = start_time
        self.end_time = end_time
        self.candles = candles
        self.nb_candles = len(candles)