class BlendMode:
    """
    Base class for blending mode. 
    Inherited classes should have overwritten `blend()` method.
    """
    def __init__(self, bits: int) -> None:
        self.bits = bits
        self.max_one = 2 ** bits - 1
        self.max_all = 2 ** (bits * 4) - 1

    def blend(self, bg, fg):
        raise NotImplementedError()
    
    def compose(self, bg, fg):
        if bg._bits != fg._bits:
            raise ValueError(f"can not blend colors with different size")
        
        return self.blend(bg, fg)
        
    
class Normal(BlendMode):
    """
    Normal blending mode.
    """
    def blend(self, bg, fg):
        from .rgba import RGBA

        alpha = fg.a / self.max_one

        return RGBA((
            (fg.r * alpha + bg.r * (1 - alpha)),
            (fg.g * alpha + bg.g * (1 - alpha)),
            (fg.b * alpha + bg.b * (1 - alpha)),
            max(fg.a, bg.a)
        ), self.bits)
    