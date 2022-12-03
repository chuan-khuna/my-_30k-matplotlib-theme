import skimage
import numpy as np
import pandas as pd


class Color:

    def __init__(self, color_hex: str):
        """_summary_

        Args:
            color_hex (str): color in hex format `#rrggbb`
        """
        self.hex = color_hex

        # convert color to other formats
        self.__to_rgb()
        self.__to_srgb()
        self.__to_luminance()
        self.__to_hsv()

    def __to_rgb(self):
        self.rgb = np.array([
            int(f"0x{self.hex[1:3]}", base=16),
            int(f"0x{self.hex[3:5]}", base=16),
            int(f"0x{self.hex[5:]}", base=16)
        ],
                            dtype=int)

    def __to_srgb(self):
        self.sRGB = np.round(self.rgb / 255.0, 4)

    def __to_luminance(self):
        # l_rgb = []
        # for color_sRGB in self.sRGB:
        #     if color_sRGB <= 0.03928:
        #         l_rgb.append(color_sRGB / 12.92)
        #     else:
        #         l_rgb.append(((color_sRGB + 0.055) / 1.055)**2.4)
        # luminance_const = np.array([0.2126, 0.7152, 0.0722])
        # self.luminance = np.sum(luminance_const * np.array(l_rgb))
        self.luminance = np.round(skimage.color.rgb2gray(self.sRGB), 4)

    def __to_hsv(self):
        # HSB: hue(0-360 degree), saturation(0-100 %), brightness(0-100 %)
        # HSV: hue, saturation, value
        self.hsv = np.round(skimage.color.rgb2hsv(self.sRGB), 4)
        self.hsb = self.hsv

        self.hsv_decimal = np.round(self.hsv * np.array([360, 100, 100]))
        self.hsb_decimal = self.hsv_decimal