import yfinance as yf
import pandas as pd
import os, csv
import datetime
import requests


num_batch_storage = "./BatchData/Numerical/yfinance/"
year = "2023"
month = "09"
interval = '2m'
# num_storage_path = "./NumericalData/"

#Stock name examples: goog, googl, bidu, baba, tsla, amzn, aapl, meta
# stock_name = 'goog'
stock_names = {'aapl', 'acn', 'acre', 'acp', 'adbe', 'agnc', 'amd', 'amzn', 'ape', 'ari', 'arr', 'asml', 'atvi', 'ba',
               'baba', 'bidu', 'cad=x', 'celh', 'clm', 'cmcsa', 'coke', 'crf', 'crm','crwd', 'csco', 'docu', 'dus',
                'dx', 'ea', 'ec', 'ecc', 'etsy', 'eurcad=x', 'eurusd=x', 'fvrr', 'gnl', 'gof', 'goog', 'ibm', 'iep',
               'intc', 'ivr', 'jnj', 'jpm', 'kdp', 'ko', 'kref', 'lumn','meta', 'mfa', 'mnst', 'msft', 'mtch', 'nflx',
                'nly', 'nvda', 'nymt', 'okta', 'orc', 'orcl', 'para', 'pbr', 'pbr-a', 'pdi', 'pep', 'pg', 'pins', 'pypl',
               'qcom', 'roku', 'shop', 'sjt', 'snap', 'sony','spot', 'sq', 'sqm', 't', 'tmus', 'tpvg', 'trin', 'trmd',
                'trtx', 'tsla', 'tsm', 'ttd', 'twlon', 'two', 'uber', 'vod', 'vz', 'wbd', 'xflt', 'yelp', 'zg', 'zm'}
#Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
period = ''
#Available intervals on yfinance: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#Intraday data cannot extend last 60 days

# start_date = '2023-08-30'
# end_date = '2023-08-31'

def collect_ticker(storage_path, stock_name, interval, start_date, end_date):
    print("Collecting ticker from Yahoo Finance")
    stock = yf.Ticker(stock_name)
    data = stock.history(interval=interval, start=start_date, end=end_date)
    # data.head()
    # print(data)
    if not os.path.exists(f'{storage_path}{stock_name}/{interval}'):
        os.makedirs(f'{storage_path}{stock_name}/{interval}')
    data.to_csv(f'{storage_path}{stock_name}/{interval}/{stock_name}_{interval}_{start_date}_to_{end_date}.csv')
    print(f"Successfully stored CSV data for {stock_name} stock, from {start_date} to {end_date} with candle interval = {interval}")


def collect_tickers_intra_timeframe(storage_path, stock_names, interval, start, end, timedelta):
    print(f"Collecting tickers from {start} to {end} in {timedelta} increments")
    for stock_name in stock_names:
        start_date = start
        end_date = start_date + timedelta
        while end_date <= end:
            collect_ticker(storage_path, stock_name, interval, start_date, end_date)
            start_date = end_date
            end_date += datetime.timedelta(days=1)
        print("Collected all stocks for:" +str(stock_name))

def delete_empty_csvs(storage_path, stock_name, interval):
    print(f"Removing empty CSV files for {stock_name}")
    for filename in os.listdir(f"{storage_path}{stock_name}/{interval}/"):
        if filename.endswith(".csv"):
            filepath = os.path.join(f"{storage_path}{stock_name}/{interval}/", filename)
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                row_count = sum(1 for row in reader)
                file.close()
                if row_count <= 1:
                    print(f"Deleting {filename} as it has only the title row.")
                    os.remove(filepath)

def delete_all_empty_csvs(storage_path, stock_names, interval):
    print("Removing empty CSV files")
    for stock_name in stock_names:
        delete_empty_csvs(storage_path, stock_name, interval)
    print("Done removing all empty CSV files")



if __name__ == '__main__':
    # print("Data Collector")
    # collect_ticker(stock_name, interval, start_date, end_date)

    # start = datetime.date(2023, 9, 1)
    # end = datetime.date(2023, 9, 30)
    # timedelta = datetime.timedelta(days=1)
    # collect_tickers_intra_timeframe(num_batch_storage, stock_names, interval, start, end, timedelta)

    delete_all_empty_csvs(num_batch_storage, stock_names, interval)

    #Code for weekly data over 5 years
    # for stock_name in stock_names:
    #     start_date = datetime.date(2018, 1, 1)
    #     end_date = datetime.date(2023, 1, 1)
    #     collect_ticker(stock_name, interval, start_date, end_date)
    #     print("Collected all stocks for:" + str(stock_name))

    # for stock_name in stock_names:
    #     start = datetime.date(2023, 8, 1)
    #     end = datetime.date(2023, 8, 31)
    #     start_date = start
    #     end_date = start_date + datetime.timedelta(days=1)
    #     while end_date <= end:
    #         collect_ticker(stock_name, interval, start_date, end_date)
    #         start_date = end_date
    #         end_date += datetime.timedelta(days=1)
    #     print("Collected all stocks for:" +str(stock_name))