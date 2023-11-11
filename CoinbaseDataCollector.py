import requests
import pandas as pd
import datetime
import os

num_storage_path = "./NumericalData/"
batch_storage = "./BatchData/Numerical/"

# Coinbase Pro API endpoint
BASE_URL = "https://api.pro.coinbase.com/products/doge-usd/candles"
API_KEY = 'Ce2fjeGMzIREx48w'
API_SECRET = 'UO8XYhl8XonDCeoH6MfQA9XPwLGi02mt'

stock_name = 'XRP-USD'
GRANULARITY = 3600


def get_historic_rates(start_date=None, end_date=None):
    print("In historic rates")
    """
    Granularity is the candle duration in seconds.
    Valid granularity values are: {60, 300, 900, 3600, 21600, 86400}
    """
    params = {
        'start': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'end': end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'granularity': GRANULARITY
    }
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SECRET": API_SECRET
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json()

# def save_to_csv(data, filename):
#     # Convert the raw data into a pandas dataframe
#     df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
#
#     # Convert UNIX timestamp to datetime
#     df['time'] = pd.to_datetime(df['time'], unit='s')
#     df.set_index('time', inplace=True)
#     df.to_csv(filename)

# CHECK CODE ABOVE, IT'S FROM GPT

if __name__ == "__main__":
    print("Coinbase Data Collector")


    #Initializing start date (and final end date, to check
    start_date = datetime.date(2021, 1, 1)
    final_date = datetime.date(2023, 8, 31)
    delta = datetime.timedelta(days=3)
    csv_count = 1
    data_frames = []

    if not os.path.exists(f'{num_storage_path}{stock_name}/{GRANULARITY}'):
        os.makedirs(f'{num_storage_path}{stock_name}/{GRANULARITY}')

    while start_date <= final_date:
        if(len(data_frames)==0):
            start_date_csv = start_date
        end_date = start_date + delta
        print(f"Fetching data from {start_date} to {end_date}")

        data = get_historic_rates(start_date, end_date)
        df = pd.DataFrame(data, columns=["Date", "Low", "High", "Open", "Close", "Volume"])
        df["Date"] = pd.to_datetime(df["Date"], unit='s')
        data_frames.append(df)

        # After 3 requests, save to CSV
        if len(data_frames) == 3:
            combined_df = pd.concat(data_frames, ignore_index=True)
            combined_df.to_csv(f"{num_storage_path}{stock_name}/{GRANULARITY}/{stock_name}_{GRANULARITY}_{start_date_csv}_{end_date}.csv", index=False)
            data_frames = []  # reset list
            csv_count += 1

        start_date = end_date  # increment start_date by 3 days

    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        combined_df.to_csv(f"{num_storage_path}{stock_name}/{GRANULARITY}/{stock_name}_{GRANULARITY}_{start_date_csv}_{end_date}.csv", index=False)


    # data = get_historic_rates()
    # save_to_csv(data, 'doge_usd_ohlc.csv')
