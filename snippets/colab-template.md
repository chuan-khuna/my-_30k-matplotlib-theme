# Prepare ENV

update/download libraries

```py
import os
from google.colab import drive

drive.mount('/content/gdrive')
google_drive_path = "/content/gdrive/MyDrive/"

# change directory to the project path
project_path = "/Colab Notebooks/..../"
os.chdir(google_drive_path + project_path)
os.listdir("./")
```

```py
# !rm -rf tmp && git clone https://github.com/chuan-khuna/my-python-utils.git tmp && cp -R tmp/utils ./ && cp -R tmp/fonts ./ && rm -rf tmp
```

```py
!pip install matplotlib seaborn -Uq
!pip install pythainlp -q

!pip install tensorflow -Uq
!pip install tensorflow-io[tensorflow] -Uq
!pip install tf2onnx onnxruntime -q
!pip install keras-tuner -q
```

```py
%load_ext tensorboard
```

# Import libraries

```py
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patheffects
import seaborn as sns
```

```py
import json
import yaml
import re
from tqdm.notebook import trange, tqdm
import datetime
```

Tensorflow things

```py
import tensorflow as tf
import tensorflow_datasets as tfds
import keras_tuner
from tensorflow.keras.layers import *

seed_ = 20200218
tf.random.set_seed(seed_)
np.random.seed(seed_)

from sklearn.metrics import confusion_matrix, classification_report
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
def check_version(version_str, major, minor):
    print(version_str)
    version = [int(i) for i in version_str.split('.')]
    assert version[0] >= major and version[1] >= minor

check_version(matplotlib.__version__, 3, 6)
check_version(sns.__version__, 0, 12)
check_version(tf.__version__, 2, 11)

del check_version

matplotlib.__version__, sns.__version__, tf.__version__
```

## View hardware spec

```py
!nvidia-smi
```

```py
# use mixed precision

policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

print('Compute dtype: %s' % policy.compute_dtype)
print('Variable dtype: %s' % policy.variable_dtype)
```

# Code

```py
print("Hello world")
```
