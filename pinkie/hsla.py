import random
from typing import Sequence


class HSLA:
    """`HSLA` (Hue, Saturation, Lightness, Alpha) color model."""

    __slots__ = ('_h', '_s', '_l', '_a')

    def __init__(self, color: Sequence[int], /) -> None:
        """
        Parameters
        ----------
        color: `Sequence[int]`
            Color sequence of h, s, l and optional a.

        Raises
        ------
        `ValueError` 
            If the color is invalid.
        """
        if isinstance(color, Sequence):
            self.h = color[0]
            self.s = color[1]
            self.l = color[2]
            self.a = color[3] if len(color) == 4 else 100
        else:
            raise ValueError(f"Invalid color value: {color}")

    def __eq__(self, other) -> bool:
        return isinstance(other, HSLA) and self.hsla == other.hsla

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"hsla{self.hsla}"

    def __repr__(self) -> str:
        return f"<HSLA h={self.h}, s={self.s}, l={self.l}, a={self.a}>"

    def __hash__(self) -> int:
        return hash(self.hsla)
            
    def __getitem__(self, key):
        return self.hsla[key]
    
    def __iter__(self):
        for item in self.hsla:
            yield item

    @property
    def h(self) -> int:
        """Hue value in range `0-359`."""
        return self._h
    
    @h.setter
    def h(self, value: int):
        value %= 360
        if value < 0:
            value += 360
        self._h = round(value)

    hue = h

    @property
    def s(self) -> int:
        """Saturation value in range `0-100`."""
        return self._s
    
    @s.setter
    def s(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._s = min(max(value, 0), 100)

    saturation = s

    @property
    def l(self) -> int:
        """Lightness value in range `0-100`."""
        return self._l
    
    @l.setter
    def l(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._l = min(max(value, 0), 100)

    lightness = l

    @property
    def a(self) -> int:
        """Alpha value (transparency) in range `0-100`."""
        return self._a
    
    @a.setter
    def a(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._a = min(max(value, 0), 100)

    alpha = a

    @property
    def hsl(self) -> tuple[int, int, int]:
        """`(h, s, l)` tuple."""
        return (self.h, self.s, self.l)
    
    @property
    def hsla(self) -> tuple[int, int, int, int]:
        """`(h, s, l, a)` tuple."""
        return (self.h, self.s, self.l, self.a)
    
    def copy(self) -> "HSLA":
        """Get a copy of the color."""
        obj = HSLA.__new__(HSLA)
        obj._h = self._h
        obj._s = self._s
        obj._l = self._l
        obj._a = self._a
        return obj

    def to_rgba(self):
        """Convert to `RGBA` model."""
        from .rgba import RGBA

        h = self.h / 360.0
        s = self.s / 100.0
        l = self.l / 100.0
        
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        if s == 0:
            r = g = b = int(l * 255)
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3) * 255
            g = hue_to_rgb(p, q, h) * 255
            b = hue_to_rgb(p, q, h - 1/3) * 255

        return RGBA((r, g, b, self.a * 2.55))

    def range(
        self, 
        num: int, 
        step: int, 
        angle: int | None = None
    ) -> list["HSLA"]:
        """
        Get a list of circular colors.

        Parameters
        ----------
        num: `int`
            Number of colors.
        step: `int`
            Step angle in degrees.
        angle: `int`
            Start angle.
        """
        angle = angle or self.h
        result = []

        for i in range(num):
            co = self.copy()
            co.h = angle + step * i
            result.append(co)

        return result

    def complementary(self) -> "HSLA":
        """Get a complementary color."""
        color = self.copy()
        color.h += 180
        return color
    
    def split_complementary(self) -> list["HSLA"]:
        """Get 2 split-complementary colors."""
        return self.range(2, 60, self.h + 150)
    
    def triadic(self) -> list["HSLA"]:
        """Get 2 triadic colors."""
        return self.range(2, 120, self.h + 120)
    
    def tetradic(self) -> list["HSLA"]:
        """Get 3 tetradic colors."""
        return self.range(3, 90, self.h + 90)
    
    def analogous(self) -> list["HSLA"]:
        """Get 3 analogous colors."""
        return self.range(3, 30, self.h - 30)
    
    @classmethod
    def random(cls) -> "HSLA":
        return cls([random.randint(0, i) for i in (360, 100, 100, 100)])