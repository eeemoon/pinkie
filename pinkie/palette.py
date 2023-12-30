from typing import Iterable


class Palette:
    """
    `RGBA` Color palette.
    """
    _web: "Palette" = None

    def __init__(self, colors: Iterable) -> None:
        """
        Palette constructor.

        Attributes
        ----------
        colors: `Iterable[RGBA]`
            List of colors.

        Raises
        ------
        `ValueError` if the any of the colors is not `RGBA` instance.
        """
        from .rgba import RGBA

        self._items: list[RGBA] = []
        self._bits: int = 0

        for color in colors:
            self.add(color)

    # magic methods
    def __eq__(self, other) -> bool:
        return isinstance(other, Palette) and all(
            first == second for first, second in zip(self, other))

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, Palette) and len(self.color) < len(other.color)
    
    def __le__(self, other):
        return isinstance(other, Palette) and len(self.color) <= len(other.color)
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other

    def __str__(self) -> str:
        return f"Palette(num={len(self._items)})"

    def __repr__(self) -> str:
        return f"<Palette colors={self._items}>"

    def __hash__(self) -> int:
        return hash(self.value)
    
    def __getitem__(self, key):
        return self._items[key]
    
    def __iter__(self):
        for item in self._items:
            yield item

    def _check(self, color):
        from .rgba import RGBA
        
        if not isinstance(color, RGBA) or (self._bits and color.bits != self._bits):
            raise ValueError("color must be instance of RGBA and have same bit count")

    # attributes
    def add(self, color) -> None:
        """
        Add a color to the palette.

        Attributes
        ----------
        color: `RGBA`
            Color to add.

        Raises
        ------
        `ValueError` if the color is invalid.
        """
        self._check(color)
        self._items.append(color)

    def remove(self, color) -> None:
        """
        Remove the color to the palette.

        Attributes
        ----------
        color: `RGBA`
            Color to remove.

        Raises
        ------
        `ValueError` if the color is not present or is invalid.
        """
        self._check(color)
        self._items.remove(color)

    # palette generators
    @staticmethod
    def web() -> "Palette":
        """
        Get a palette of web-safe colors.
        """
        from .rgba import RGBA

        if Palette._web is None:
            Palette._web = [
                RGBA((i * 51, j * 51, k * 51)) 
                for i in range(6) 
                for j in range(6) 
                for k in range(6)
            ]
        
        return Palette(Palette._web)
    
    @staticmethod
    def random(num: int) -> "Palette":
        """
        Generate a palette with random colors.

        Attributes
        ----------
        num: `int`
            Number of colors.
        """
        from .hsla import HSLA

        return Palette(HSLA.random().to_rgba() for _ in range(num))
    
    @staticmethod
    def gradient(start, end, num: int) -> "Palette":
        """
        Generate a palette with colors that create gradient from start to end.

        Attributes
        ----------
        start: `RGBA`
            Start color.
        end: `RGBA`
            End color.
        num: `int`
            Number of colors.

        Raises
        ------
        `ValueError` if the number < 2.
        """
        from .rgba import RGBA

        if num < 2:
            raise ValueError("number of colors must be greater than or equal to 2")

        def interpolate(start, end, step):
            return int(start + (end - start) * step)
        
        gradient = []
        for i in range(num):
            step = i / (num - 1) 

            color = RGBA((
                interpolate(start.r, end.r, step),
                interpolate(start.g, end.g, step),
                interpolate(start.b, end.b, step),
                interpolate(start.a, end.a, step)
            ))
           
            gradient.append(color)

        return Palette(gradient)