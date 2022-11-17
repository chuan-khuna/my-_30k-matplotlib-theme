# My Python code snippets and libraries

## `.gitignore`

```txt
.DS_Store
.ipynb_checkpoints
*.pyc
Untitled.ipynb
Untitled[a-zA-Z0-9].ipynb
```

## Basic import

```py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patheffects
import seaborn as sns
```

## To import theme

```py
from utils.vis_utils import *
```

## To clone utils

```txt
rm -rf tmp && git clone https://github.com/chuan-khuna/my-python-utils.git tmp && cp -R tmp/utils ./ && rm -rf tmp
```

## To run unit tests

[many ways](https://docs.pytest.org/en/7.1.x/how-to/output.html) to run `pytest`

```sh
python3 -m pytest ./tests --cov
```

you can add

```sh
--tb=short
--tb=no
```
