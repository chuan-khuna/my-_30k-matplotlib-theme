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

# Model training Report

```py
def my_model_report(hist,
                    metrics: list[str],
                    labels_dict: dict[str, dict[str, list]],
                    conf_ticks: list[str],
                    fig_title: str = "",
                    save_path: str = "",
                    row_h: float = 2.5,
                    dpi: int = 100):

    # extract metrics in tensorflow's hist obj
    metrics_in_hist = []
    for k in hist.history.keys():
        if not k.startswith('val_'):
            metrics_in_hist.append(k)
    metrics = [metric for metric in metrics if metric in metrics_in_hist]

    # create plot template
    fig_h = (len(metrics) + 1) * row_h
    conf_mosaic = [['conf_train', 'conf_val', 'conf_test']]
    fig_mosaic = [[metric] * 3 for metric in metrics]
    fig, axs = plt.subplot_mosaic(fig_mosaic + conf_mosaic, figsize=(fig_h, fig_h), dpi=dpi)

    plt.suptitle(fig_title)

    # plot epoch history
    epochs = hist.epoch
    for metric in metrics:
        sns.lineplot(x=epochs, y=hist.history[metric], label=metric, ax=axs[metric])

        val_metric = 'val_' + metric
        if val_metric in hist.history.keys():
            sns.lineplot(x=epochs, y=hist.history[val_metric], label=val_metric, ax=axs[metric])
            axs[metric].grid(True, alpha=0.2)

    # plot confusion matrix
    valid_keys = ['train', 'val', 'test']
    for k in list(labels_dict.keys()):
        if k in valid_keys:
            data = labels_dict[k]
            if 'true' in list(data.keys()) and 'pred' in list(data.keys()):
                true_labels = data['true']
                pred_labels = data['pred']
                sns.heatmap(confusion_matrix(true_labels, pred_labels),
                            annot=True,
                            fmt='d',
                            square=True,
                            cbar=False,
                            ax=axs[f'conf_{k}'],
                            xticklabels=conf_ticks,
                            yticklabels=conf_ticks)
                axs[f'conf_{k}'].set_title(f'confusion matrix {k}')

    for k in valid_keys:
        if k not in list(labels_dict.keys()):
            axs[f'conf_{k}'].axis('off')

    axs['conf_train'].set_title('confusion matrix train')
    axs['conf_train'].set_xlabel('pred')
    axs['conf_train'].set_ylabel('actual')

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    plt.show()


valid_keys = ['train', 'val', 'test']
for k in list(labels_dict.keys()):
    if k in valid_keys:
        data = labels_dict[k]
        if 'true' in list(data.keys()) and 'pred' in list(data.keys()):
            true_labels = data['true']
            pred_labels = data['pred']
            report_text = classification_report(true_labels, pred_labels)
            print(report_text)
```
