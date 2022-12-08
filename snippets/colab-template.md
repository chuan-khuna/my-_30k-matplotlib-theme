# Prepare ENV

update/download libraries

```py
# !rm -rf tmp && git clone https://github.com/chuan-khuna/my-python-utils.git tmp && cp -R tmp/utils ./ && cp -R tmp/fonts ./ && rm -rf tmp
```

```py
!pip install matplotlib seaborn -Uq
!pip install pythainlp -q
```

# Mount Google Drive

```py
import os
from google.colab import drive

drive.mount('/content/gdrive')
google_drive_path = "/content/gdrive/MyDrive/"
```

```py
# change directory to the project path

project_path = "/Colab Notebooks/.../"
os.chdir(google_drive_path + project_path)
os.listdir("./")
```

# Import libraries

```py
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patheffects
import seaborn as sns

import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report

import json
import re
from tqdm.notebook import trange, tqdm
```

import my libraries

```py
from utils.vis_utils import *
from utils.preprocessing.text.text_cleaner import TextCleaner
from utils.preprocessing.text.tweet_cleaner import TweetCleaner

mpl_import_fonts("./fonts/")
```

check libraries version

```py
matplotlib.__version__, sns.__version__, tf.__version__
```
