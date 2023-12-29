class BlendMode:
    """
    The base class for blending modes. 
    Inherited classes should have overwritten `blend()` method.
    """
    def __init__(self, bits: int) -> None:
        self.bits = bits
        self.max_one = 2 ** bits - 1
        self.max_all = 2 ** (bits * 4) - 1

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float):
        """
        Method called to calculate the result value for each channel.
        All values are in range `0-1`.

        Attributes
        ----------
        bg: `float`
            Background channel value.
        fg: `float`
            Foreground channel value.
        bg_a: `float`
            Background alpha value.
        fg_a: `float`
            Foreground alpha value.
        """
        raise NotImplementedError()
    
    def comp(self, co: float, a: float):
        """
        Get a premultiplied color value with its complementary alpha.

        Attributes
        ----------
        co: `float`
            Color channel value.
        a: `float`
            Alpha value.
        """
        return co * (1 - a)
    
    def compose(self, bg, fg):
        """
        Compose 2 colors.

        Attributes
        ----------
        bg: `Color`
            Background color.
        fg: `Color`
            Foreground color.
        """
        from .rgba import RGBA

        if bg.bits != fg.bits:
            raise ValueError(f"can not blend colors with different size")
        
        maxv = self.max_one
        bg_a = bg.a / maxv
        fg_a = fg.a / maxv

        return RGBA((
            self.blend(bg.r / maxv, fg.r / maxv, bg_a, fg_a) * maxv,
            self.blend(bg.g / maxv, fg.g / maxv, bg_a, fg_a) * maxv,
            self.blend(bg.b / maxv, fg.b / maxv, bg_a, fg_a) * maxv,
            max(bg.a, fg.a)
        ), self.bits)
        
    
class Normal(BlendMode):
    """
    Normal blending mode.
    """
    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float):
        return fg * fg_a + self.comp(bg, fg_a)
    

class Multiply(BlendMode):
    """
    Multiply blending mode.
    """
    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float):
        return fg * bg + self.comp(fg, bg_a) + self.comp(bg, fg_a)
    

class Screen(BlendMode):
    """
    Screen blending mode.
    """
    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float):
        return 1 - (1 - bg * bg_a) * (1 - fg * fg_a)
    