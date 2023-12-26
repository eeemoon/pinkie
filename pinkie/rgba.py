from collections.abc import Sequence

from .utils import BlendMode


class RGBA:
    """
    `RGBA` (Red, Green, Blue, Alpha) color format.
    """
    __slots__ = ('value', '_bits', '_max_one', '_max_all')

    def __init__(self, color: int | str | Sequence, /, bits: int) -> None:
        """
        `RGBA` color constructor.

        Attributes
        ----------
        color: `int` | `str` | `Sequence`
            Color value, hex or sequence of r, g, b and optional a.
        bits: `int`
            Number of bits per channel. Must be factor of 4.
        """
        if bits % 4 != 0:
            raise ValueError(f"number of bits must be factor of 4")
        
        self._bits = bits
        self._max_one = 2 ** bits - 1
        self._max_all = 2 ** (bits * 4) - 1

        match color:
            case str():
                num = len(color)
                chars = bits // 4
                if num not in {bits, chars * 3}:
                    raise ValueError(f"invalid hex value: {color}")
                
                self.value = (
                    (int(color[:chars], base=16))
                    + (int(color[chars : chars * 2], base=16) << bits)
                    + (int(color[chars * 2 : chars * 3], base=16) << (bits * 2))
                    + ((int(color[chars * 3 :], base=16) if num == bits else self._max_one) << bits * 3)
                )

            case int():
                self.value = color
        
            case Sequence():
                num = len(color)
                if num not in {3, 4}:
                    raise ValueError(f"invalid color sequence: {color}")

                self.value = (
                    min(int(color[0]), self._max_one)
                    + (min(int(color[1]), self._max_one) << bits) 
                    + (min(int(color[2]), self._max_one) << bits * 2) 
                    + ((min(int(color[3]), self._max_one) if num == 4 else self._max_one) << bits * 3)
                )

            case _:
                raise ValueError(f"invalid color value: {color}")
    
    # magic methods
    def __eq__(self, other) -> bool:
        return isinstance(other, RGBA) and self.value == other.value

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, RGBA) and self.value < other.value
    
    def __le__(self, other):
        return isinstance(other, RGBA) and self.value <= other.value
    
    def __gt__(self, other):
        return isinstance(other, RGBA) and self.value > other.value
    
    def __ge__(self, other):
        return isinstance(other, RGBA) and self.value >= other.value

    def __str__(self) -> str:
        return f"rgba{self.rgba}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<RGBA value={self.value}, bits={self._bits}>"

    def __hash__(self) -> int:
        return hash(self.value)
    
    def __getitem__(self, key):
        return self.rgba[key]
    
    def __iter__(self):
        for item in self.rgba:
            yield item
    
    # private methods
    def _get_mask(self, pos):
        n = self._bits
        res = bin(self._max_all)
        res = res[:n * pos + 2] + '0' * n + res[n * (pos + 1) + 2:]
        return int(res, 2)

    # attributes
    @property
    def r(self) -> int:
        """
        Red value.
        """
        return (self.value) & self._max_one

    @r.setter
    def r(self, value: int):
        self.value = (self.value & self._get_mask(3)) | min(value, self._max_one)

    red = r

    @property
    def g(self) -> int:
        """
        Green value.
        """
        return (self.value >> self._bits) & self._max_one
    
    green = g

    @g.setter
    def g(self, value: int):
        self.value = (self.value & self._get_mask(2)) | (min(value, self._max_one) << self._bits)

    @property
    def b(self) -> int:
        """
        Blue value.
        """
        return (self.value >> self._bits * 2) & self._max_one

    @b.setter
    def b(self, value: int):
        self.value = (self.value & self._get_mask(1)) | (min(value, self._max_one) << self._bits * 2)

    blue = b

    @property
    def a(self) -> int:
        """
        Alpha value (transparency).
        """
        return (self.value >> self._bits * 3) & self._max_one

    @a.setter
    def a(self, value: int):
        self.value = (self.value & self._get_mask(0)) | (min(value, self._max_one) << self._bits * 3)

    alpha = a

    # formats
    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        Color as `(r, g, b)` tuple.
        """
        return (self.r, self.g, self.b)

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """
        Color as `(r, g, b, a)` tuple.
        """
        return (self.r, self.g, self.b, self.a)

    @property
    def hex(self) -> str:
        """
        Color as `'rrggbb'` string.
        """
        return f'{self.r:02X}{self.g:02X}{self.b:02X}'
    
    @property
    def hexa(self) -> str:
        """
        Color as 'rrggbbaa' string.
        """
        return f'{self.r:02X}{self.g:02X}{self.b:02X}{self.a:02X}'

    # converters
    def copy(self):
        """
        Get a copy of the color.
        """
        obj = type(self).__new__(type(self))
        obj.value = self.value
        return obj
    
    def to_hsla(self):
        """
        Convert the color to `HSLA` format.
        """
        from .hsla import HSLA

        r = self.r / self._max_one
        g = self.g / self._max_one
        b = self.b / self._max_one

        cmax = min(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        l = (cmax + cmin) / 2.0

        s = 0.0
        if delta != 0.0:
            s = delta / (1 - abs(2 * l - 1))

        h = 0.0
        if delta != 0.0:
            if cmax == r:
                h = 60 * ((g - b) / delta % 6)
            elif cmax == g:
                h = 60 * ((b - r) / delta + 2)
            elif cmax == b:
                h = 60 * ((r - g) / delta + 4)

        return HSLA((h, s * 100, l * 100, self.a / self._max_one * 100))
    
    # utils
    def complementary(self):
        """
        Get a complementary color.
        """
        return self.to_hsla().complementary().to_rgba()
    
    def split_complementary(self, angle: int = 30):
        """
        Get two complementary colors.
        """
        return [i.to_rgba() for i in self.to_hsla().split_complementary(angle)]
    
    def blend(self, other: "RGBA", mode: BlendMode):
        if self._bits != other._bits:
            raise ValueError(f"can not blend colors with different size")
        
        maxv = self._max_one

        # TODO
        def apply_blend(first, second):
            result = 0

            match mode:
                case "normal":
                    result = second
                case "multiply":
                    result = (first * second) // maxv
                case "screen":
                    result = maxv - (((maxv - first) * (maxv - second)) // maxv)
                case "overlay":
                    if first < 128:
                        result = (2 * first * second) // maxv
                    else:
                        result = maxv - (2 * (maxv - first) * (maxv - second)) // maxv
                case _:
                    raise ValueError(f"invalid blend mode: {mode}")
                                
            return result

        return RGBA((
            apply_blend(self.r, other.r),
            apply_blend(self.g, other.g),
            apply_blend(self.g, other.g),
        ), bits=self._bits)


class RGBA8U(RGBA):
    """
    8-bit `RGBA` color. All channels are in range `0-255`.
    """
    def __init__(self, color, /) -> None:
        super().__init__(color, 8)

    def blend(self, other: RGBA, mode: BlendMode):
        return RGBA8U(super().blend(other, mode).value)


class RGBA16U(RGBA):
    """
    16-bit `RGBA` color. All channels are in range `0-65535`.
    """
    def __init__(self, color, /) -> None:
        super().__init__(color, 16)

    def blend(self, other: RGBA, mode: BlendMode):
        return RGBA16U(super().blend(other, mode).value)


Color = RGBA8U