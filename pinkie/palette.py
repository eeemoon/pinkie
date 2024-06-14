from __future__ import annotations

from .rgba import RGBA


class Palette:
    """`RGBA` Color palette."""

    _web: Palette | None

    def __init__(self, *colors: RGBA) -> None:
        """
        Palette constructor.

        Parameters
        ----------
        *colors: `RGBA`
            List of colors.

        Raises
        ------
        `ValueError` 
            If any of colors is not `RGBA` instance.
        """
        self._items: list[RGBA] = []
        self._bits: int | None = None

        for color in colors:
            self.add_color(color)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Palette) 
            and len(self) == len(other)
            and all(first == second for first, second in zip(self, other))
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"Palette(num={len(self._items)})"

    def __repr__(self) -> str:
        return f"<Palette colors={self._items}>"
    
    def __getitem__(self, key):
        return self._items[key]
    
    def __iter__(self):
        for item in self._items:
            yield item

    @property
    def bits(self) -> int | None:
        return self._bits
    
    @bits.setter
    def bits(self, value: int | None):
        if isinstance(value, int):
            if value % 4 != 0 or value < 4:
                raise ValueError("Number of bits must be dividable by 4")
        elif not isinstance(value, None):
            raise ValueError("Invalid value")
        
        self._bits = value

    def add_color(self, color: RGBA, /) -> None:
        """
        Add a color to the palette.

        Parameters
        ----------
        color: `RGBA`
            Color to add.

        Raises
        ------
        `ValueError`
            If the color is invalid.
        """
        if not isinstance(color, RGBA) or (self.bits and color.bits != self.bits):
            raise ValueError("Color must be RGBA and have same bit count as the palette")
        
        self._items.append(color)

        if not self.bits:
            self.bits = color.bits

    def remove_color(self, color: RGBA) -> None:
        """
        Remove the color from the palette.

        Parameters
        ----------
        color: `RGBA`
            Color to remove.

        Raises
        ------
        `ValueError` 
            If the color is not present.
        """
        self._items.remove(color)

        if len(self._items) == 0:
            self.bits = None

    @classmethod
    def web(cls) -> "Palette":
        """Get a palette of web-safe colors."""
        if cls._web is None:
            cls._web = cls(*(
                RGBA((i * 51, j * 51, k * 51)) 
                for i in range(6) 
                for j in range(6) 
                for k in range(6)
            ))
        
        return cls._web
    
    @classmethod
    def random(cls, num: int) -> "Palette":
        """
        Generate a palette with random colors.

        Parameters
        ----------
        num: `int`
            Number of colors.
        """
        return cls(*(RGBA.random() for _ in range(num)))
    
    @classmethod
    def gradient(cls, start: RGBA, end: RGBA, num: int) -> "Palette":
        """
        Generate a palette with colors that create gradient.

        Parameters
        ----------
        start: `RGBA`
            Start color.
        end: `RGBA`
            End color.
        num: `int`
            Number of colors.

        Raises
        ------
        `ValueError`
            If the number < 2.
        """
        if num < 2:
            raise ValueError("Number of colors must be greater than or equal to 2")

        gradient = [
            RGBA((
                int(start.r + (end.r - start.r) * (i / (num - 1))),
                int(start.g + (end.g - start.g) * (i / (num - 1))),
                int(start.b + (end.b - start.b) * (i / (num - 1))),
                int(start.a + (end.a - start.a) * (i / (num - 1)))
            ))
            for i in range(num)
        ]

        return Palette(*gradient)
    