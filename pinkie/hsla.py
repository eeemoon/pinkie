import random
from collections.abc import Sequence


class HSLA:
    """
    `HSLA` (Hue, Saturation, Lightness, Alpha) color model.
    """
    __slots__ = ('_h', '_s', '_l', '_a')

    def __init__(self, color: Sequence, /) -> None:
        """
        `RGBA` color constructor.

        Attributes
        ----------
        color: `Sequence`
            Color sequence of h, s, l and optional a.
        """
        match color:
            case tuple() | list():
                self.h = color[0]
                self.s = color[1]
                self.l = color[2]
                self.a = color[3] if len(color) == 4 else 100
            case _:
                raise ValueError(f"invalid color value: {color}")
    
    # magic methods
    def __eq__(self, other) -> bool:
        return isinstance(other, HSLA) and self.hsla == other.hsla

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, HSLA) and self.s + self.a < other.s + other.a
    
    def __le__(self, other):
        return isinstance(other, HSLA) and self.s + self.a <= other.s + other.a
    
    def __gt__(self, other):
        return isinstance(other, HSLA) and self.s + self.a > other.s + other.a
    
    def __ge__(self, other):
        return isinstance(other, HSLA) and self.s + self.a >= other.s + other.a

    def __str__(self) -> str:
        return f"hsla{self.hsla}"

    def __repr__(self) -> str:
        return f"<HSLA h={self.h}, s={self.s}, l={self.l}, a={self.a}>"

    def __hash__(self) -> int:
        h = hash(self.h)
        s = hash(self.s)
        l = hash(self.l)
        a = hash(self.a)

        return h ^ s ^ l ^ a
            
    def __getitem__(self, key):
        return self.hsla[key]
    
    def __iter__(self):
        for item in self.hsla:
            yield item

    # attributes
    @property
    def h(self) -> int:
        """
        Hue value in range `0-359`.
        """
        return self._h
    
    @h.setter
    def h(self, value: int):
        self._h = round(value % 360)

    hue = h

    @property
    def s(self) -> int:
        """
        Saturation value in range `0-100`.
        """
        return self._s
    
    @s.setter
    def s(self, value: int):
        self._s = min(round(value), 100)

    saturation = s

    @property
    def l(self) -> int:
        """
        Lightness value in range `0-100`.
        """
        return self._l
    
    @l.setter
    def l(self, value: int):
        self._l = min(round(value), 100)

    lightness = l

    @property
    def a(self) -> int:
        """
        Alpha value (transparency) in range `0-100`.
        """
        return self._a
    
    @a.setter
    def a(self, value: int):
        self._a = min(round(value), 100)

    alpha = a

    # formats
    @property
    def hsl(self) -> tuple[int, int, int]:
        """
        Color as `(h, s, l)` tuple.
        """
        return (self.h, self.s, self.l)
    
    @property
    def hsla(self) -> tuple[int, int, int, int]:
        """
        Color as `(h, s, l, a)` tuple.
        """
        return (self.h, self.s, self.l, self.a)
    
    # converters
    def copy(self) -> "HSLA":
        """
        Get a copy of the color.
        """
        obj = HSLA.__new__(HSLA)
        obj._h = self._h
        obj._s = self._s
        obj._l = self._l
        obj._a = self._a

        return obj

    def to_rgba(self):
        """
        Convert the color to `RGBA` model.
        """
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

    # utils
    def complementary(self) -> "HSLA":
        color = self.copy()
        color.h += 180
        return color
    
    def range(self, num: int = 2, angle: int = 360) -> list["HSLA"]:
        ang = angle / (num + 1)
        result = []

        compl = self.complementary()

        for i in range(0, num):
            a = ang * i + ang

            current = compl.copy()
            current.h += a

            result.append(current)
            
        return result
    
    @staticmethod
    def random(
        h: tuple[int, int] = (0, 359),
        s: tuple[int, int] = (0, 100),
        l: tuple[int, int] = (0, 100),
        a: tuple[int, int] = (0, 100)
    ):
        return HSLA([
            random.randint(*i) if isinstance(i, tuple) else i
            for i in (h, s, l, a)
        ])