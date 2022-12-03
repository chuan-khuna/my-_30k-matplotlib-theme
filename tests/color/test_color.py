import pytest
from utils.color.color import Color
# my Color class should be a skimage color wrapper


def test_initialise_color_by_hex():
    c = Color('#202f66')


def test_color_should_contain_these_attributes():
    c = Color('#202f66')
    assert isinstance(c.hex, str)

    # test rgb pair should be in range 0-255
    assert len(c.rgb) == 3
    for val in c.rgb:
        assert val >= 0 and val <= 255

    assert c.luminance

    # aliases
    assert all(c.hsb == c.hsv)
