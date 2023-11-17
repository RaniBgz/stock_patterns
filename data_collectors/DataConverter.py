import plotly.graph_objects as go

import pandas as pd
import os
from datetime import datetime
import shutil

num_batch_storage = "./BatchData/Numerical/yfinance/"
candle_batch_storage = "./BatchData/Candlestick/yfinance/"
dataset_storage_path = "./datasets/inference/inference_dataset_sept2023_2m/images/train/"
res_width = 1280
res_height = 720

# stock_name = 'XRP-USD'
interval = '2m'
stock_names = {'aapl', 'acn', 'acre', 'adbe', 'agnc', 'amd', 'amzn', 'ari', 'asml', 'atvi', 'ba',
               'baba', 'bidu', 'cad=x', 'celh', 'cmcsa', 'crm','crwd', 'csco', 'docu',
                'dx', 'ea', 'ec', 'etsy', 'eurcad=x', 'eurusd=x', 'fvrr', 'gnl', 'goog', 'ibm', 'iep',
               'intc', 'ivr', 'jnj', 'jpm', 'kdp', 'ko','meta', 'mnst', 'msft', 'mtch', 'nflx',
                'nly', 'nvda', 'okta', 'orc', 'orcl', 'para', 'pbr', 'pbr-a', 'pep', 'pg', 'pins', 'pypl',
               'qcom', 'roku', 'shop', 'snap', 'sony','spot', 'sq', 'sqm', 't', 'tmus',
                'tsla', 'tsm', 'ttd', 'two', 'uber', 'vz', 'wbd','yelp', 'zg', 'zm'}

# crypto_stock_names = {'DOGE-USD', 'BTC-USD', 'ETH-USD'}

#Goes through numerical storage folder, then specific stock subfolder
#Generates pyplot graph from CSV
def plot_candlestick_from_csv(stock_name, num_storage_path, candle_storage_path):
    for csv_file in os.listdir(f'{num_storage_path}{stock_name}/{interval}'):
        df = pd.read_csv(f'{num_storage_path}{stock_name}/{interval}/{csv_file}')

        # df.index = pd.to_datetime(df['Date'], utc=True)
        # Save the candlestick chart as a PNG image
        # mpf.plot(df, type='candle', savefig=dict(fname=candle_storage_path + stock_name + '/' + csv_file.replace('.csv', '.png'), dpi=300, pad_inches=0.25))

        # print(df)
        if(interval=='1d' or interval=='5d' or interval=='1wk' or interval=='1mo' or interval=='3mo' or interval=="3600"):
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
        # fig.show()

        # Create subdirectory if it doesn't exist
        if not os.path.exists(f"{candle_storage_path}{stock_name}/{interval}/{res_width}"):
            os.makedirs(f"{candle_storage_path}{stock_name}/{interval}/{res_width}")

        # Save the image
        fig.write_image(f"{candle_storage_path}{stock_name}/{interval}/{res_width}/" + csv_file.replace('.csv', '.png'))
        print("Stored candlestick for " +str(stock_name))


def transfer_all_files_to_dataset(stock_names, interval, src, dst):
    for stock_name in stock_names:
        transfer_files_to_dataset(stock_name, interval, src, dst)

def transfer_files_to_dataset(stock_name, interval, src, dst):
    source_directory = f'{src}{stock_name}/{interval}/{res_width}'

    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory {source_directory} does not exist. Skipping...")
        return

    # Ensure the destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)

    # If the source directory exists, proceed with copying the files
    for img_file in os.listdir(source_directory):
        shutil.copy(f'{source_directory}/{img_file}', f'{dst}/{img_file}')

    # if not os.path.exists(f'{dst}'):
    #     os.makedirs(f'{dst}')
    # for img_file in os.listdir(f'{src}{stock_name}/{interval}/{res_width}'):
    #     shutil.copy(f'{src}{stock_name}/{interval}/{res_width}/{img_file}',f'{dst}/{img_file}')


def plot_all_candlesticks(stock_names, num_storage_path, candle_storage_path):
    for stock_name in stock_names:
        plot_candlestick_from_csv(stock_name, num_storage_path, candle_storage_path)



if __name__ == '__main__':
    print("Data Converter")

    # plot_all_candlesticks(stock_names, num_batch_storage, candle_batch_storage)
    transfer_all_files_to_dataset(stock_names, interval, candle_batch_storage, dataset_storage_path)
    # transfer_files_to_dataset(candle_storage_path, dataset_storage_path, stock_name, interval)

    # for stock_name in stock_names:
    #     transfer_files_to_dataset(candle_storage_path, dataset_storage_path, stock_name, interval)
    #     # plot_candlestick_from_csv(stock_name)
    #     print("Done drawing candlesticks for " +str(stock_name))
