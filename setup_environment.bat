mkdir BatchData
mkdir BatchData/Numerical
mkdir BatchData/Candlestick
mkdir RealTimeData
mkdir RealTimeData/Numerical
mkdir RealTimeData/Candlestick
mkdir RealTimeResults
conda update -n base -c defaults conda -y
conda create -n stock_patterns python=3.8 -y
conda activate stock_patterns
pip install -r requirements.txt