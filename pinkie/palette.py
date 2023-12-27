
class Palette:
    _web = None

    def __init__(self, colors: list) -> None:
        from .rgba import RGBA

        self._colors = []

        for c in colors:
            if not isinstance(c, RGBA):
                raise ValueError("colors must be instances of RGBA")
            
            self._colors.append(c)

    @property
    def colors(self):
        return self._colors.copy()

    @staticmethod
    def web():
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