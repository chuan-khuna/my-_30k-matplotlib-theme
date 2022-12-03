import pytest
from utils.color.color import Color
import numpy as np
# my Color class should be a skimage color wrapper


@pytest.fixture
def colors():
    c1, c2 = Color('#202f66'), Color('#ff7048')
    yield c1, c2
    del c1
    del c2


def test_initialise_color_by_hex():
    c = Color('#202f66')


def test_other_formats_updated_after_setting_color_hex():
    c = Color('#202f66')
    old_value = c.__dict__.copy()

    c.hex = '#ff7048'
    new_value = c.__dict__
    for k in old_value.keys():
        res = old_value[k] != new_value[k]
        if isinstance(res, (bool, np.bool_)):
            assert res
        else:
            assert all(res)

    c.hex = '#202f66'
    new_value = c.__dict__
    for k in old_value.keys():
        res = old_value[k] == new_value[k]
        if isinstance(res, (bool, np.bool_)):
            assert res
        else:
            assert all(res)


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


def test_repr_function(colors):
    c1, c2 = colors
    # at least, calling this object in Jupyter lab
    # should be readable by human
    assert c1.hex in c1.__repr__()
    assert c2.hex in c2.__repr__()


# Test calling functions to calculate
# various type of colour distance metrics
# error should not occur


def test_calculate_distance_between_colors(colors):
    c1, c2 = colors

    # calculate by using Color object
    c1.distance(c2)

    # calculate by using hex string
    c1.distance(c2.hex)


def test_calculate_delta_e_between_colors(colors):
    c1, c2 = colors

    # calculate by using Color object
    c1.delta_e(c2)

    # calculate by using hex string
    c1.delta_e(c2.hex)


def test_calculate_wcag_contrast_between_colors(colors):
    c1, c2 = colors

    # calculate by using Color object
    c1.wcag_contrast(c2)

    # calculate by using hex string
    c1.wcag_contrast(c2.hex)