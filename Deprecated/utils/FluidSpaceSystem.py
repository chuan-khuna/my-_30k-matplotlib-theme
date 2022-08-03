import numpy as np


def to_list(array):
    return np.round(np.array(array, dtype=np.float), 2).tolist()


class FluidSpace:
    """[summary]
    This class is in spired by https://utopia.fyi/.

    Calculate the size of element (in pt) which proportionally scale to a given length. 
    """

    def __init__(self, length=1, space=25, scale=1.618, n_scale=(2, 2)):
        assert length > 0 and isinstance(length, (int, float))
        assert space > 0 and isinstance(space, int)
        assert scale > 1 and isinstance(scale, float)
        assert len(n_scale) == 2 and isinstance(n_scale, (tuple, list, np.ndarray))

        self.ppi = 72

        self.length = length
        self.space = space
        self.n_scale = n_scale
        self.scale = scale
        self._update()

    def how(self):
        self._update()
        print(f"""\
1 pt = 1/72 inch
PPI = point per inch
inch -> point: inch * PPI
pt -> px: pt * (1/72) * DPI
-----
- devided {self.length} inch into {self.space} equal spaces.
- each space = {self.unit_space}(inch, % of length) 
  or {self.space_pt}pt
- scale = {self.scale}
- the base space size is {self.space_pt}pt
-----
- scales = {to_list(self.scales)}
- spaces (pt) = {to_list(self.spaces)}
""")

    def _update(self):
        self.scales = np.round(self.scale**np.arange(-self.n_scale[0], self.n_scale[1] + 1), 3)
        self.unit_space = np.round(self.length / self.space, 3)
        self.space_pt = np.round(self.unit_space * self.ppi, 2)
        self.spaces = np.round(self.scales * self.space_pt, 2)
        self.spaces_percent = np.round(self.scales * self.unit_space, 3)

    def set_space(self, space):
        assert space > 0 and isinstance(space, int)
        self.space = space
        self._update()

    def set_length(self, length):
        assert length > 0 and isinstance(length, (int, float))
        self.length = length
        self._update()

    def set_scale(self, scale):
        assert scale > 1 and isinstance(scale, float)
        self.scale = scale
        self._update()

    def set_n_scale(self, n_scale):
        assert len(n_scale) == 2 and isinstance(n_scale, (tuple, list, np.ndarray))
        self.n_scale = n_scale
        self._update()