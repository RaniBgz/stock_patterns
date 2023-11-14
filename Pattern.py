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


    def __str__(self):
        return f'Pattern : {self.name} was detected with confidence : {self.confidence}.' \
               f' It started at time: {self.start_time} and ended at {self.end_time}.' \
               f' It contains {self.nb_candles} candles'