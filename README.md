# stock_patterns

# Before creating the environment
Install Anaconda or MiniConda (https://docs.anaconda.com/free/anaconda/install/index.html)


# Setup folder structure
``` sh
start setup_environment.bat
```
# Automatic installation: Update Anaconda, install environment and dependencies: to do in a conda command prompt


# Manual installation: Update Anaconda, install environment and dependencies: to do in a conda command prompt
``` sh
conda update -n base -c defaults conda -y
conda create -n stock_patterns python=3.8 -y
conda activate stock_patterns
pip install -r requirements.txt
```