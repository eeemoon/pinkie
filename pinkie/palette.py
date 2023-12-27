class Palette:
    _web = None

    def __init__(self, colors: list) -> None:
        from .rgba import RGBA

        self.colors = []
        self._bits = 0

        for c in colors:
            if not isinstance(c, RGBA) or (self._bits and c.bits != self._bits):
                raise ValueError("colors must be instances of RGBA")
            
            self.colors.append(c)

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
        return f"Palette(num={len(self.colors)})"

    def __repr__(self) -> str:
        return f"<Palette colors={self.colors}>"

    def __hash__(self) -> int:
        return hash(self.value)
    
    def __getitem__(self, key):
        return self.colors[key]
    
    def __iter__(self):
        for item in self.colors:
            yield item

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
        from .hsla import HSLA

        return Palette(HSLA.random().to_rgba() for _ in range(num))
    
    @staticmethod
    def gradient(start, end, num: int) -> "Palette":
        from .rgba import RGBA

        if num < 2:
            raise ValueError("number of colors can not be smaller than 2")

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