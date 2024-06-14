import random
from typing import Sequence

from .utils import distance


class RGBA:
    """RGBA (Red, Green, Blue, Alpha) color model."""

    __slots__ = ('_data', '_bits', '_max_one', '_max_all')

    def __init__(self, color: int | str | Sequence[int], /, bits: int = 8) -> None:
        """
        Parameters
        ----------
        color: `int` | `str` | `Sequence[int]`
            Decimal value, hex or a sequence of r, g, b and optional a.
        bits: `int`
            Number of bits per channel. Must be dividable by 4.
            Defaults to 8 bits, which equals 256 values per channel.

        Raises
        ------
        `ValueError`
            If the color is invalid.
        """
        self.bits: int = bits
        self._max_one: int = (1 << bits) - 1
        self._max_all: int = (1 << (bits * 4)) - 1

        if isinstance(color, int):
            self._data = (color & self._max_all) | (self._max_one << (self.bits * 3))
        elif isinstance(color, str):
            color = color.removeprefix('#')
            
            per_channel = self.bits // 4
            if len(color) not in {per_channel * 3, per_channel * 4}:
                raise ValueError(f"Invalid hex value: {color}")
            
            if len(color) == per_channel * 3:
                color += 'F' * per_channel
            
            self._data = int(color, 16)
        elif isinstance(color, Sequence):
            if len(color) not in {3, 4} or not all(isinstance(i, int) for i in color):
                raise ValueError(f"Invalid color sequence: {color}")
            
            if len(color) == 3:
                color = (*color, self._max_one)
            
            self._data = sum(
                min(max(c, 0), self._max_one) << (num * self.bits) 
                for num, c in enumerate(color)
            )
        else:
            raise ValueError(f"Invalid color value: {color}")

    def __eq__(self, other) -> bool:
        return isinstance(other, RGBA) and self._data == other._data

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"rgba{self.rgba}"

    def __int__(self) -> int:
        return self._data

    def __repr__(self) -> str:
        return f"<RGBA value={self._data}, bits={self.bits}>"

    def __hash__(self) -> int:
        return hash(self._data)
    
    def __getitem__(self, key):
        return self.rgba[key]
    
    def __iter__(self):
        for item in self.rgba:
            yield item

    def _channel_value(self, pos: int) -> int:
        return (self._data >> (pos * self.bits)) & self._max_one

    def _set_channel_value(self, pos: int, value: int) -> None:
        val = min(max(value, 0), self._max_one)
        shift = pos * self.bits
        mask = ~(self._max_one << shift)
        self._data = (self._data & mask) | (val << shift)

    @property
    def bits(self) -> int:
        return self._bits
    
    @bits.setter
    def bits(self, value: int):
        if value % 4 != 0 or value < 4:
            raise ValueError("Number of bits must be dividable by 4")
        
        self._bits = value

    @property
    def r(self) -> int:
        """Red value."""
        return self._channel_value(3)

    @r.setter
    def r(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._set_channel_value(3, value)

    red = r

    @property
    def g(self) -> int:
        """Green value."""
        return self._channel_value(2)

    @g.setter
    def g(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._set_channel_value(2, value)

    green = g

    @property
    def b(self) -> int:
        """Blue value."""
        return self._channel_value(1)

    @b.setter
    def b(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._set_channel_value(1, value)

    blue = b

    @property
    def a(self) -> int:
        """Alpha value (transparency)."""
        return self._channel_value(0)

    @a.setter
    def a(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an int, not {type(value).__name__}")
        self._set_channel_value(0, value)

    alpha = a

    @property
    def rgb(self) -> tuple[int, int, int]:
        """`(r, g, b)` tuple."""
        return self.r, self.g, self.b

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """`(r, g, b, a)` tuple."""
        return self.r, self.g, self.b, self.a

    @property
    def hex(self) -> str:
        """HEX string."""
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"
    
    @property
    def hexa(self) -> str:
        """HEX string with alpha."""
        return f"{self.r:02X}{self.g:02X}{self.b:02X}{self.a:02X}"
    
    @property
    def decimal(self) -> int:
        """Integer value of RGBA."""
        return self._data
    
    @property
    def value(self) -> int:
        """Integer value of RGB. Does not contain alpha."""
        return self._data >> self.bits

    def copy(self) -> "RGBA":
        """Get a copy of the color."""
        obj = RGBA.__new__(RGBA)
        obj._data = self._data
        obj._bits = self._bits
        return obj
    
    def to_hsla(self):
        """Convert to `HSLA` color model."""
        from .hsla import HSLA

        r, g, b = (c / self._max_one for c in self.rgb)
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        l = (cmax + cmin) / 2
        s = delta / (1 - abs(2 * l - 1)) if delta != 0 else 0
        h = 0
        if delta != 0:
            if cmax == r:
                h = 60 * ((g - b) / delta % 6)
            elif cmax == g:
                h = 60 * ((b - r) / delta + 2)
            elif cmax == b:
                h = 60 * ((r - g) / delta + 4)

        return HSLA((
            round(h), 
            round(s * 100), 
            round(l * 100), 
            round(self.a / self._max_one * 100)
        ))
    
    def to_cmyk(self):
        """Convert to `CMYK` color model."""
        from .cmyk import CMYK

        rgb = self.rgb
        cmax = max(rgb)
        k = 1 - cmax / self._max_one

        if k == 1:
            return CMYK((0, 0, 0, 100))
        
        c, m, y = ((1 - i / self._max_one - k) / (1 - k) for i in rgb)

        return CMYK([round(i * 100) for i in [c, m, y, k]])
    
    def convert(self, bits: int) -> "RGBA":
        """
        Convert the color to another bit count.

        Parameters
        ----------
        bits: `int`
            Number of bits per channel. Must be dividable by 4. 
        """
        scale = (1 << bits) // (1 << self.bits)
        maxv = (1 << bits) - 1
        return RGBA([min(i * scale, maxv) for i in self.rgba], bits=bits)
    
    def normalize(self) -> tuple[float, float, float, float]:
        """Normalize RGBA to `0-1` range."""
        return tuple(i / self._max_one for i in self.rgba)
    
    def brightness(self) -> int:
        """Get a perceived brightness in range `0-1`."""
        r, g, b, _ = self.normalize()
        return 0.299 * r ** 2 + 0.587 * g ** 2 + 0.114 * b ** 2

    def is_light(self, threshold: float = 0.5) -> bool:
        """
        Determines if color is light based on HSP color model.

        Parameters
        ----------
        threshold: `float`
            Brightness threshold.
        """
        return self.brightness() > threshold
            
    def complementary(self) -> "RGBA":
        """Get the complementary color."""
        return self.to_hsla().complementary().to_rgba()
    
    def split_complementary(self) -> list["RGBA"]:
        """Get 2 split-complementary colors."""
        return [i.to_rgba() for i in self.to_hsla().split_complementary()]
    
    def triadic(self) -> list["RGBA"]:
        """Get 2 triadic colors."""
        return [i.to_rgba() for i in self.to_hsla().triadic()]
    
    def tetradic(self) -> list["RGBA"]:
        """Get 3 tetradic colors."""
        return [i.to_rgba() for i in self.to_hsla().tetradic()]
    
    def analogous(self) -> list["RGBA"]:
        """Get 3 analogous colors."""
        return [i.to_rgba() for i in self.to_hsla().analogous()]
    
    def closest(self, *colors: "RGBA") -> "RGBA":
        """
        Select the closest color to this one.

        Parameters
        ----------
        *colors: `RGBA`
            List of colors.

        Raises
        ------
        `ValueError` 
            If no colors specified.
        """        
        if len(colors) == 0:
            raise ValueError("Specify at least 1 color")

        return min(colors, key=lambda c: distance(self, c))
    
    def furthest(self, *colors: "RGBA") -> "RGBA":
        """
        Select the furthest color to this one.

        Parameters
        ----------
        *colors: `RGBA`
            List of colors.

        Raises
        ------
        `ValueError` 
            If no colors specified.
        """        
        if len(colors) == 0:
            raise ValueError("Specify at least 1 color")

        return max(colors, key=lambda c: distance(self, c))
    
    # TODO
    def blend(self, other: "RGBA", mode) -> "RGBA":
        """
        Blend the color with another one. 
        Second color will be placed on top of this.

        Parameters
        ----------
        other: `RGBA`
            Foreground color.
        mode: `BlendMode`
            Blending mode. Must be a child class of `BlendMode`.

        Raises
        ------
        `ValueError` 
            If the mode is invalid or bit counts of the colors do not match.
        """
        from .blend import BlendMode

        if not issubclass(mode, BlendMode):
            raise ValueError(f"blend mode must be inherited from the {BlendMode.__name__} class")

        return mode(self.bits).compose(self, other)
    
    @classmethod
    def random(cls, bits: int = 8) -> "RGBA":
        """
        Generate a random color.

        Parameters
        ----------
        bits: `int`
            Number of bits.
        """
        return cls(
            [random.randint(0, 2 ** bits - 1) for _ in range(4)], 
            bits=bits
        )


Color = RGBA