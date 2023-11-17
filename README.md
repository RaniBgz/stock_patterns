## Stock Patterns: Downloading stock data from YFinance and recognizing patterns

### Before creating the environment:
Install Anaconda or MiniConda (https://docs.anaconda.com/free/anaconda/install/index.html)


### Automatic installation:
This script does everything:

-Creates the directories to store the data and results

-Updates Anaconda, creates environment, activates it

-Installs the required dependencies
``` sh
start setup_environment.bat
```

### 2-step installation:
The script above may stop or be blocked after the first conda call due to having several calls in a row.

A better way to install is to do the directories part automatically by launching this script in an Anaconda Prompt:
``` sh
start create_directories.bat
```
After that, you can type the commands one by one and wait for them to execute. If your Anaconda install is already up to date,
you can skip the first line.
``` sh
conda update -n base -c defaults conda -y
conda create -n stock_patterns python=3.8 -y
conda activate stock_patterns
pip install -r requirements.txt
```

If all else fails, here are all the manual commands. You can check the requirements.txt files to see the necessary pip packages
### Fully manual installation:
``` sh
mkdir BatchData
mkdir BatchData\Numerical
mkdir BatchData\Candlestick
mkdir RealTimeData
mkdir RealTimeData\Numerical
mkdir RealTimeData\Candlestick
mkdir RealTimeResults
mkdir yolo
mkdir yolo\weights
conda update -n base -c defaults conda -y
conda create -n stock_patterns python=3.8 -y
conda activate stock_patterns
pip install -r requirements.txt
```

### Transferring the yolo weights
If you are pulling this repo from git, chances are the model weights are not included.

Before being able to use the model, you should put your YoloV8 weights in the yolo/weights directory

The YoloDetector.py script has a variable that points to the weights:

``` sh
yolo_weights = "./yolo/weights/yoloL_90_3p.pt"
```
Adjust this variable accordingly based on your yolo weights


### Deactivating and removing the environment

To deactivate the environment use:
``` sh
conda deactivate
``` 

To remove it, use the following command after deactivating it:
``` sh
conda remove --name stock_patterns --all -y 
```

To check how to use the code, please refer to HOW_TO_USE_IT.md