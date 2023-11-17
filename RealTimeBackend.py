'''
This script recovers data from Yahoo Finance for all the stocks in stock_names, runs a Yolo inference, and
'''
import yfinance as yf
import pandas as pd
import os, csv
import datetime as dt
from datetime import datetime
import time
import plotly.graph_objects as go
import argparse

#Custom imports
import YoloDetector as yd
from Frame import Frame
from Candle import Candle
from TimeInterval import TimeInterval

#Setting paths to data
rt_storage_path = "./RealTimeData/"
num_rt_storage_path = rt_storage_path + "/Numerical/"
candle_rt_storage_path = rt_storage_path + "/Candlestick/"

#Defining candle duration
interval = '2m'

#Defining the size of the window (= number of hours) for each frame
window = 12

#Set the names of the stock you want to query here
stock_names = ['aapl', 'goog', 'meta', 'nvda', 'tsla']

#Switch to True to continuously parse stock(s). If interval is equal to 2min, stock/stocks will be acquired every 2m and so on
continuous_loop = True

#Set to True to save image with predicted bounding box (debug), False otherwise (production)
save_predicted_imgs = True

#Resolution of the image that is built
res_width = 1280
res_height = 720

# Create the parser
# parser = argparse.ArgumentParser(description='Process some stock data.')
#
# # Add arguments
# parser.add_argument('interval', type=str, help='The interval for stock data')
# parser.add_argument('stock_names', type=str, nargs='+', help='A list of stock names')
# parser.add_argument('--save_predicted_imgs', action='store_true', help='Flag to save predicted images')
# parser.add_argument('--continuous_loop', action='store_true', help='Flag to keep the process running in a loop')
#
# # Parse the arguments
# args = parser.parse_args()

class BackendProcess:
    def __init__(self, num_storage, candle_storage, interval, stock_names, save_predicted_imgs, continuous_loop):
        self.num_storage = num_storage
        self.candle_storage = candle_storage
        self.interval = TimeInterval(interval)
        self.stock_names = stock_names
        self.yolo_detector = yd.YoloDetector(save_predicted_imgs)
        self.continuous_loop = continuous_loop


    def collect_tickers_and_detect_loop(self):
        while(True):
            print(f"Collecting tickers at time={datetime.now()}")
            self.collect_tickers_and_detect()
            time.sleep(self.interval.minutes*60)

    def collect_tickers_and_detect(self):
        for stock_name in self.stock_names:
            #Collects ticker, creates and stores a CSV file
            start_time, end_time, num_rows = self.collect_ticker(stock_name)

            # Check if there is sufficient data
            if num_rows < 10:
                continue  # Skip to the next iteration if data is insufficient

            #Creates a PNG based on the CSV file, creates a Frame object for Yolo detection
            frame = self.plot_candlestick_from_time(stock_name, start_time, end_time)

            #Calls Yolo detector on Frame
            bounding_boxes = []
            bounding_boxes = self.yolo_detector.detect_patterns_on_image(frame)

            if bounding_boxes is not None and bounding_boxes != []:
                # If patterns are detected, convert BoundingBox2D to Patterns and add them to the Frame
                frame.convert_bb2d_to_patterns(bounding_boxes)
                #Displaying patterns highest high and lowest low
                frame.display_patterns_highest_high()
                frame.display_patterns_lowest_low()


    def collect_and_store_ticker(self):
        for stock_name in self.stock_names:
            start_time, end_time = self.collect_ticker(self.num_storage, stock_name, self.interval)
            self.plot_candlestick_from_time(stock_name, self.num_storage, self.candle_storage, start_time, end_time)


    def collect_ticker(self, stock_name):
        #Getting current time and setting start time as 1 day before the current time
        current_time = datetime.now()
        timedelta = dt.timedelta(hours=window)
        start_time = current_time-timedelta

        #Collecting data
        print(f"Collecting ticker from Yahoo Finance from {start_time} to {current_time}")
        stock = yf.Ticker(stock_name)
        data = stock.history(interval=self.interval.interval, start=start_time, end=current_time)

        # Check if data is empty or has less than 8 lines of data
        num_rows = len(data)
        if num_rows == 0 or num_rows < 8:
            print(f"Insufficient data for {stock_name} ({num_rows} rows). Skipping.")
            return start_time, current_time, num_rows

        #Converting time format
        start_time = start_time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        current_time = current_time.strftime("%Y-%m-%d_%Hh%Mm%Ss")

        if not os.path.exists(f'{self.num_storage}{stock_name}/{self.interval.interval}'):
            os.makedirs(f'{self.num_storage}{stock_name}/{self.interval.interval}')
        data.to_csv(f'{self.num_storage}{stock_name}/{self.interval.interval}/{stock_name}_{self.interval.interval}_{start_time}_to_{current_time}.csv')
        # print(f"Successfully stored CSV data for {stock_name} stock, from {start_date} to {end_date} with candle interval = {interval}")
        return start_time, current_time, num_rows


    def plot_candlestick_from_time(self, stock_name, start_time, end_time):
        #Loading CSV and converting it to Pandas data frame
        csv_file = f'{stock_name}_{self.interval.interval}_{start_time}_to_{end_time}.csv'
        csv_path = f'{self.num_storage}{stock_name}/{self.interval.interval}/{csv_file}'
        df = pd.read_csv(csv_path)

        # Parsing CSV data to build a PNG and storing it
        img_path = self.build_and_store_png_from_csv(stock_name, df, csv_file)

        #Extracting candles from CSV
        candles = self.extract_candles_from_pandas_frame(df)

        # stock_name, interval, start_time, end_time, candles, nb_candles, csv_path, img_path, patterns)
        frame = Frame(stock_name, self.interval, start_time, end_time, candles, len(candles), csv_path, img_path, res_width, res_height, [])

        #Printing frame information
        # print(frame.__str__())
        return frame


    def extract_candles_from_pandas_frame(self, df):
        candles = []
        # Convert the Datetime column to datetime objects
        df['Datetime'] = pd.to_datetime(df['Datetime'])

        # Iterate over DataFrame rows
        for index, row in df.iterrows():
            # Create a Candle object for each row
            candle = Candle(
                start_time=row['Datetime'],
                interval=interval,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            # Append the Candle object to the list
            candles.append(candle)
        return candles


    def build_and_store_png_from_csv(self, stock_name, df, csv_file):
        # Parsing CSV data to build a PNG and storing it TODO: Create some sort of enum to have a global logic of intervals values
        one_day = TimeInterval("1d")
        #If Time interval is greater than one day, first row is named "Date"
        if (self.interval.__ge__(one_day)):
            fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                 open=df['Open'],
                                                 high=df['High'],
                                                 low=df["Low"],
                                                 close=df['Close'])])
        #Otherwise, it is named Datetime
        else:
            fig = go.Figure(data=[go.Candlestick(x=df['Datetime'],
                                                 open=df['Open'],
                                                 high=df['High'],
                                                 low=df["Low"],
                                                 close=df['Close'])])

        fig.update_layout(
            xaxis=dict(showticklabels=False, zeroline=False, showgrid=False, visible=True,
                       rangeslider=dict(visible=False)),
            yaxis=dict(showticklabels=False, zeroline=False, showgrid=False, visible=True),
            autosize=False,
            margin=dict(t=0, r=0, b=0, l=0),
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=res_width,
            height=res_height,
        )

        # Storing PNG in the right folder
        if not os.path.exists(f"{self.candle_storage}{stock_name}/{self.interval.interval}/{res_width}"):
            os.makedirs(f"{self.candle_storage}{stock_name}/{self.interval.interval}/{res_width}")
        image_path = f"{self.candle_storage}{stock_name}/{self.interval.interval}/{res_width}/" + csv_file.replace('.csv',
                                                                                                               '.png')
        fig.write_image(image_path)
        return image_path


if __name__ == '__main__':
    backend_process = BackendProcess(num_rt_storage_path, candle_rt_storage_path, interval, stock_names, save_predicted_imgs, continuous_loop)
    if(backend_process.continuous_loop):
        backend_process.collect_tickers_and_detect_loop()
    else:
        backend_process.collect_tickers_and_detect()
