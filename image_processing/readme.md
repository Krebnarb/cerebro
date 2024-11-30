# Pre-Reqs
* Python 3 is installed
* Make sure you are in a python virtual envirnment
```shell
# Windows
python -m venv myenv
myenv\Scripts\activate

# Mac/Linux
you know what to do
```
* Get your API key from OPENCAGE and put it into **./image_processing/.env**  as
* If .env file does not exist, create it first in your ./image_processing directory
```
OPENCAGE_API_KEY=aaabbb11123
```

# Installation
```shell
cd image_processing

## activate your Python virtual environment first, then execute the following commands
pip install -r requirements.txt

python geo_plot.py "C:\Path\To\Your\Photos"