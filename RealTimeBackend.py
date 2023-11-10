'''
This script recovers data from Yahoo Finance for all the stocks in stock_names, runs a Yolo inference, and
'''
import yfinance as yf
import pandas as pd
import os, csv
import datetime as dt
from datetime import datetime
import plotly.graph_objects as go
import YoloDetector as yd

#Setting paths to data
rt_storage_path = "./RealTimeData/"
num_rt_storage_path = rt_storage_path + "/Numerical/"
candle_rt_storage_path = rt_storage_path + "/Candlestick/"

#Setting paths to Yolo results
results_base_path = './RealTimeResults/'

#Defining stock intervals, window (in hours), stock_names to monitor (stock_name when only doing tests on one stock)
interval = '2m'
window = 12
stock_names = {'aapl', 'acn', 'acre'}
stock_name = 'aapl'

#Set to True to save image with predicted bounding box (debug), False otherwise (production)
save_predicted_imgs = True

res_width = 1280
res_height = 720

class BackendProcess:
    def __init__(self, num_storage, candle_storage, interval, stock_names, stock_name, results_base_path, save_predicted_imgs):
        self.num_storage = num_storage
        self.candle_storage = candle_storage
        self.interval = interval
        self.stock_names = stock_names
        self.stock_name = stock_name
        self.yolo_detector = yd.YoloDetector(results_base_path, save_predicted_imgs)


    def collect_and_store_ticker(self):
        start_time, end_time = self.collect_ticker(self.num_storage, self.stock_name, self.interval)
        self.plot_candlestick_from_time(self.stock_name, self.num_storage, self.candle_storage, start_time, end_time)


    def collect_tickers_and_detect(self):
        start_time, end_time = self.collect_ticker()
        image_path = self.plot_candlestick_from_time(start_time, end_time)
        self.yolo_detector.detect_patterns_on_image(image_path, self.stock_name)


    def collect_ticker(self):
        #Getting current time and setting start time as 1 day before the current time
        current_time = datetime.now()
        timedelta = dt.timedelta(hours=12)
        start_time = current_time-timedelta

        #Collecting data
        print(f"Collecting ticker from Yahoo Finance from {start_time} to {current_time}")
        stock = yf.Ticker(self.stock_name)
        data = stock.history(interval=self.interval, start=start_time, end=current_time)
        # data.head()

        #Converting time format
        start_time = start_time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        current_time = current_time.strftime("%Y-%m-%d_%Hh%Mm%Ss")

        if not os.path.exists(f'{self.num_storage}{self.stock_name}/{self.interval}'):
            os.makedirs(f'{self.num_storage}{self.stock_name}/{self.interval}')
        data.to_csv(f'{self.num_storage}{self.stock_name}/{self.interval}/{self.stock_name}_{self.interval}_{start_time}_to_{current_time}.csv')
        # print(f"Successfully stored CSV data for {stock_name} stock, from {start_date} to {end_date} with candle interval = {interval}")
        return start_time, current_time


    def plot_candlestick_from_time(self, start_time, end_time):
        csv_file = f'{self.stock_name}_{self.interval}_{start_time}_to_{end_time}.csv'
        df = pd.read_csv(f'{self.num_storage}{self.stock_name}/{self.interval}/{csv_file}')
        nb_candles = len(df)

        if(self.interval=='1d' or self.interval=='5d' or self.interval=='1wk' or self.interval=='1mo' or self.interval=='3mo' or self.interval=="3600"):
            fig = go.Figure(data = [go.Candlestick(x=df['Date'],
                                                   open=df['Open'],
                                                   high=df['High'],
                                                   low=df["Low"],
                                                   close=df['Close'])])
        else:
            fig = go.Figure(data = [go.Candlestick(x=df['Datetime'],
                                                   open=df['Open'],
                                                   high=df['High'],
                                                   low=df["Low"],
                                                   close=df['Close'])])

        fig.update_layout(
            xaxis=dict(showticklabels=False, zeroline=False, showgrid=False, visible=True, rangeslider=dict(visible=False)),
            yaxis=dict(showticklabels=False, zeroline=False, showgrid=False, visible=True),
            autosize=False,
            margin = dict(t=0, r=0, b=0, l=0),
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=res_width,
            height=res_height,
        )
        if not os.path.exists(f"{self.candle_storage}{self.stock_name}/{self.interval}/{res_width}"):
            os.makedirs(f"{self.candle_storage}{self.stock_name}/{self.interval}/{res_width}")

        image_path = f"{self.candle_storage}{self.stock_name}/{self.interval}/{res_width}/" + csv_file.replace('.csv', '.png')
        fig.write_image(image_path)
        print("Stored candlestick for " + str(self.stock_name))
        return image_path



if __name__ == '__main__':
    backend_process = BackendProcess(num_rt_storage_path, candle_rt_storage_path, interval, stock_names, stock_name, results_base_path, save_predicted_imgs)
    backend_process.collect_tickers_and_detect()
    print("Detecting stock patterns in real-time")
    # collect_ticker(num_rt_storage_path, stock_name, interval)
    # collect_and_store_ticker(num_rt_storage_path, candle_rt_storage_path, stock_name, interval)