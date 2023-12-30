import random
from typing import Sequence


class CMYK:
    """
    `CMYK` (Cyan, Magenta, Yellow, Black Key) color model.
    """
    __slots__ = ('_c', '_m', '_y', '_k')

    def __init__(self, color: Sequence, /) -> None:
        """
        `CMYK` color constructor.

        Attributes
        ----------
        color: `Sequence`
            Color sequence of c, m, y, k.

        Raises
        ------
        `ValueError` if the color is invalid.
        """
        match color:
            case tuple() | list():
                self.c = color[0]
                self.m = color[1]
                self.y = color[2]
                self.k = color[3]
            case _:
                raise ValueError(f"invalid color value: {color}")
            
    # magic methods
    def __eq__(self, other) -> bool:
        return isinstance(other, CMYK) and self.cmyk == other.cmyk

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"cmyk{self.cmyk}"

    def __repr__(self) -> str:
        return f"<CMYK c={self.c}, m={self.m}, y={self.y}, k={self.k}>"

    def __hash__(self) -> int:
        c = hash(self.c)
        m = hash(self.m)
        y = hash(self.y)
        k = hash(self.k)

        return c ^ m ^ y ^ k
            
    def __getitem__(self, key):
        return self.cmyk[key]
    
    def __iter__(self):
        for item in self.cmyk:
            yield item
            
    # attributes
    @property
    def c(self) -> int:
        """
        Cyan value in range `0-100`.
        """
        return self._c
    
    @c.setter
    def c(self, value: int):
        self._c = min(round(value), 100)

    cyan = c
            
    @property
    def m(self) -> int:
        """
        Magenta value in range `0-100`.
        """
        return self._m
    
    @m.setter
    def m(self, value: int):
        self._m = min(round(value), 100)

    magenta = m

    @property
    def y(self) -> int:
        """
        Yellow value in range `0-100`.
        """
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = min(round(value), 100)

    yellow = y

    @property
    def k(self) -> int:
        """
        Black key in range `0-100`.
        """
        return self._k
    
    @k.setter
    def k(self, value: int):
        self._k = min(round(value), 100)

    key = k
    black = k

    @property
    def cmyk(self) -> tuple[int, int, int, int]:
        """
        Color as `(c, m, y, k)` tuple.
        """
        return (self.c, self.m, self.y, self.k)
    
    # converters
    def copy(self) -> "CMYK":
        """
        Get a copy of the color.
        """
        obj = CMYK.__new__(CMYK)
        obj._c = self._c
        obj._m = self._m
        obj._y = self._y
        obj._k = self._k

        return obj

    def to_rgba(self):
        """
        Convert the color to `RGBA` model.
        """
        from .rgba import RGBA

        return RGBA([
            255 * (1 - i / 100) * (1 - self.k / 100)
            for i in self.cmyk[:3]
        ])
    
    # color generators
    @staticmethod
    def random() -> "CMYK":
        return CMYK([
            random.randint(0, 100)
            for _ in range(4)
        ])
    