mkdir RealTimeData
mkdir RealTimeData\Numerical
mkdir RealTimeData\Candlestick
mkdir RealTimeResults
mkdir yolo
mkdir yolo\weights
call conda update -n base -c defaults conda -y
call conda create -n stock_patterns python=3.8 -y
call conda activate stock_patterns
call pip install -r requirements.txt