from utils.color.palette import extract_palette
import os
import pandas as pd

THIS_PATH = os.path.dirname(__file__)

# To extract a colour palette from an image
# A function take `image_path` as input
# It will return a data frame of colour palette


def test_extract_palette():
    img_path = os.path.join(THIS_PATH, "misc/Wednesday_room.jpg")
    df = extract_palette(img_path, max_width=64, deltaE_threshold=40)
    assert isinstance(df, pd.DataFrame)