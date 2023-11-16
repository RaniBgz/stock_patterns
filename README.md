# stock_patterns

### Before creating the environment:
Install Anaconda or MiniConda (https://docs.anaconda.com/free/anaconda/install/index.html)


### Automatic installation: Setup folder structure, install conda environment and dependencies (to execute in Anaconda Prompt)
``` sh
start setup_environment.bat
```

### Manual installation:
``` sh
mkdir BatchData
mkdir BatchData\Numerical
mkdir BatchData/Candlestick
mkdir RealTimeData
mkdir RealTimeData/Numerical
mkdir RealTimeData/Candlestick
mkdir RealTimeResults
conda update -n base -c defaults conda -y
conda create -n stock_patterns python=3.8 -y
conda activate stock_patterns
pip install -r requirements.txt
```

To deactivate the environment use:
``` sh
conda deactivate
``` 

To remove it, use the following command after deactivating it:
``` sh
conda remove --name stock_patterns --all -y 
```
