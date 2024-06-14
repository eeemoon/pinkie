import random
from typing import Sequence


class CMYK:
    """
    `CMYK` (Cyan, Magenta, Yellow, Black Key) color model.
    """

    __slots__ = ('_c', '_m', '_y', '_k')

    def __init__(self, color: Sequence[int], /) -> None:
        """
        Parameters
        ----------
        color: `Sequence[int]`
            Color sequence of c, m, y, k.

        Raises
        ------
        `ValueError` 
            If the color is invalid.
        """
        if isinstance(color, (tuple, list)):
            self.c = color[0]
            self.m = color[1]
            self.y = color[2]
            self.k = color[3]
        else:
            raise ValueError(f"Invalid color value: {color}")
            
    def __eq__(self, other) -> bool:
        return isinstance(other, CMYK) and self.cmyk == other.cmyk

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"cmyk{self.cmyk}"

    def __repr__(self) -> str:
        return f"<CMYK c={self.c}, m={self.m}, y={self.y}, k={self.k}>"

    def __hash__(self) -> int:
        return hash(self.cmyk)
            
    def __getitem__(self, key):
        return self.cmyk[key]
    
    def __iter__(self):
        for item in self.cmyk:
            yield item
            
    @property
    def c(self) -> int:
        """Cyan value in range `0-100`."""
        return self._c
    
    @c.setter
    def c(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._c = min(max(value, 0), 100)

    cyan = c
            
    @property
    def m(self) -> int:
        """Magenta value in range `0-100`."""
        return self._m
    
    @m.setter
    def m(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._m = min(max(value, 0), 100)

    magenta = m

    @property
    def y(self) -> int:
        """Yellow value in range `0-100`."""
        return self._y
    
    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._y = min(max(value, 0), 100)

    yellow = y

    @property
    def k(self) -> int:
        """Black key in range `0-100`."""
        return self._k
    
    @k.setter
    def k(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._k = min(max(value, 0), 100)

    key = k
    black = k

    @property
    def cmyk(self) -> tuple[int, int, int, int]:
        """`(c, m, y, k)` tuple."""
        return self.c, self.m, self.y, self.k
    
    def copy(self) -> "CMYK":
        """Get a copy of the color."""
        obj = CMYK.__new__(CMYK)
        obj._c = self._c
        obj._m = self._m
        obj._y = self._y
        obj._k = self._k
        return obj

    def to_rgba(self):
        """Convert to `RGBA` model."""
        from .rgba import RGBA

        return RGBA([
            255 * (1 - i / 100) * (1 - self.k / 100)
            for i in self.cmyk[:3]
        ])
    
    @classmethod
    def random(cls) -> "CMYK":
        """Generate a random color."""
        return cls([random.randint(0, 100) for _ in range(4)])
    