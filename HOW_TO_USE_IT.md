## Stock Patterns - How to use it

The main script to run is:
``` sh
RealTimeBackend.py
```

For now, all of the parameters have to be modified inside the script, but there are only 5 parameters that matter:

### Interval
``` sh
interval = '2m'
```
=> Defines the size of the candles to use.

The system has been tested a lot on 2 minute candles, and this is what the Yolo model is trained on,
so best results are expected for this interval.


### Window
``` sh
window = 12
```
=> Defines the number of hours for which candles are collected to build an image

Default is 12 hours, but if you are getting the "insufficient data" error a lot,
you can try increasing this. This error happens because non-crypto markets are often closed at night, leading to empty data.
By increasing the window, you will collect more candles per frame. Too few and too many candles may impact performance.
It takes generalizing the model on a lot of data to perform at all time frame.

### Stock Names
``` sh
stock_names = ['aapl', 'goog', 'meta', 'nvda', 'tsla']
```

=> List of stock names to collect

These stocks have to exist on Yahoo Finance, and the identifier has to be correct.
You can refer to the Yahoo Finance website to find stocks you are interested in: https://finance.yahoo.com/
Crypto and currency stocks are also supported, but you might have to tweak the window length, since these stocks
don't stop at night => leads to more candles in the same time frame

### Continuous loop

``` sh
continuous_loop = True
```

=> Boolean that allows the system to run continuously (True) or just once over the list of stocks (False)

If the candle size is set to "2m", the system will:

- Collect all the stocks in stock_names
- Store the data to CSV
- Build PNG images using Pandas
- Run Yolo detection on each image
- Return information about the detected patterns
- Wait for the duration of "interval" (in this example, 2 minutes)
- Query the stocks again and repeat the process

### Save predicted images

``` sh
save_predicted_imgs = True
```
=> Determines whether the Yolo images with the bounding boxes are saved.

By default, all PNG (and CSV) are stored (could be optimized in the future).

When Yolo performs a detection, it can output a visual image with the bounding box for each pattern
(and associated confidence). This is useful for human evaluation, but not necessary when running
in real-time and working with numerical data. Set this flag to "False" to avoid storing additional data

### Code organization
The important scripts for the real-time part are:

``` sh
RealTimeBackend.py
TimeInterval.py
YoloDetectory.py
BoundingBox2D.py
Frame.py
Pattern.py
Candle.py
```

### Other scripts
I have included the scripts used to collect Batch Data that is used to re-train yolo:
``` sh
DataCollector.py
CoinbaseDataCollector.py
DataConverter.py
```

The script used to retrain yolo with a custom dataset is also included. Paths have to be changed, and a yolo-format
dataset has to be available
``` sh
yolo_train.py
```

In the utils folder are a few scripts that have been useful to manipulate data and merge yolo datasets:
``` sh
DatasetCleaner.py
YoloMerger.py
```

The test folder contains a script that was used to test yolo detection
``` sh
RecognizePatterns.py
```


### Avenues for improvement


This project is just a basic proof of concept for pattern detection in real-time using YoloV8.

There are many avenues for improvement such as:
- Supporting other stock markets seamlessy with more abstracted data collectors and extractors
- Optimizing data storage by only storing images with non-duplicated patterns (Temporal logic, pattern comparison)
- If you are working with an external database with stock information: adding a connector to get that data, and getting rid of the CSVs altogether.
- Detecting duplicate patterns: Yolo will sometimes detect the same pattern twice with a different bounding box, this can be manually checked and corrected
- Extracting different and more useful numerical data from the patterns and between different patterns (Averages, specific formulas, leveraging volume)
- Training Yolo on more data and heterogeneous data (various candle sizes, currently only a few dozen weekly candles have been used in training, the rest is 2-min)
- Adding a "StrategySimulator" module that could use historical data, yolo detection and some parameters to test various strategies
(collecting data on different candle granularity, performing operations between patterns, identifying optimal buy-sell points)
- Multimodal AI: Training a model on time series and numerical data to work in concert with Yolo's visual information to gain more understanding of the markets
- Inter-stock correlations: Running models between different stocks and finding correlations between moves of different stocks:
using moves on one stock to predict moves on other stocks
- Use of language, sentiment analysis, and scrape news sites and internet to use as an additional prediction of stocks moves



