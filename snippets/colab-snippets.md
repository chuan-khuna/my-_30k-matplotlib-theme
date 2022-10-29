# Install TF

Use `-q`

```txt
# !pip3 install tensorflow==2.8.2 tensorflow-gpu==2.8.2 tensorflow-datasets -U
# !pip3 install -U seaborn matplotlib
# !pip3 install pythainlp attacut
# !pip3 install dvc
```

# numpy and pandas

```py
import numpy as np
import pandas as pd

# visualisation
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patheffects
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')
```

# Google Drive

```py
import os
from google.colab import drive
drive.mount('/content/gdrive')
google_drive_path = "/content/gdrive/MyDrive/"
```

## Set project path

```py
# change directory to the project path
# project_path = "/Colab Notebooks/..."
# os.chdir(google_drive_path + project_path)
# os.listdir("./")
```

# Tensorflow

```py
# modelling utils
import tensorflow as tf
import tensorflow_datasets as tfds

# set seed
seed_ = 20200218
tf.random.set_seed(seed_)
np.random.seed(seed_)

from sklearn.metrics import confusion_matrix, classification_report
```

```py
# load fonts
font_dir = [f"{google_drive_path}/code_assets/fonts/"]
for font in matplotlib.font_manager.findSystemFonts(font_dir):
    matplotlib.font_manager.fontManager.addfont(font)

# Override Metric with Google Outfit
# matplotlib.rcParams['font.family'] = 'outfit'
```

# Info

```py
tf.config.list_physical_devices('GPU')

for device in tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(device, True)
```

```txt
!nvidia-smi
```

# Use TQDM with notebook

https://tqdm.github.io/docs/notebook/
