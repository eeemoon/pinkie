class BlendMode:
    """
    The base class for blending modes. 
    Inherited classes must have overwritten `blend()` method.
    """

    def __init__(self, bits: int) -> None:
        self.bits = bits
        self.max_one = 2 ** bits - 1
        self.max_all = 2 ** (bits * 4) - 1

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        """
        Calculate the result value for each channel.
        All arguments are in range `0-1`.

        Parameters
        ----------
        bg: :class:`float`
            Background channel value.
        fg: `float`
            Foreground channel value.
        bg_a: `float`
            Background alpha value.
        fg_a: `float`
            Foreground alpha value.
        """
        raise NotImplementedError("blend mode class must have implemented 'blend' method")
    
    def comp(self, co: float, a: float) -> float:
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
        bg: `RGBA`
            Background color.
        fg: `RGBA`
            Foreground color.

        Raises
        ------
        `ValueError` if bit counts of the colors do not match.
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
            (bg_a + fg_a - bg_a * fg_a) * maxv
        ), self.bits)
        

class Normal(BlendMode):
    """
    Normal blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return fg * fg_a + self.comp(bg, fg_a)
    

class Darken(BlendMode):
    """
    Darken blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return min(fg * bg_a, bg * fg_a) + self.comp(fg, bg_a) + self.comp(bg, fg_a);


class Multiply(BlendMode):
    """
    Multiply blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return fg * bg + self.comp(fg, bg_a) + self.comp(bg, fg_a)
    

class ColorBurn(BlendMode):
    """
    Color Burn blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        if fg == 0:
            if bg == bg_a:
                return fg_a * bg_a + self.comp(bg, fg_a)
            else:
                return self.comp(bg, fg_a)
        else:
            return (
                bg_a * fg_a + self.comp(fg, bg_a) + self.comp(bg, fg_a)
                - min(fg_a * bg_a, ((bg_a * fg_a - bg * fg_a) / fg * bg_a))
            )


class Lighten(BlendMode):
    """
    Lighten blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return max(fg * bg_a, bg * fg_a) + self.comp(fg, bg_a) + self.comp(bg, fg_a);
    

class Screen(BlendMode):
    """
    Screen blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return 1 - (1 - bg * bg_a) * (1 - fg * fg_a)


class ColorDodge(BlendMode):
    """
    Color Dodge blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        if fg == fg_a:
            if bg == 0:
                return self.comp(fg, bg_a);
            else:
                return fg_a * bg_a + self.comp(fg, bg_a) + self.comp(bg, fg_a);
        else:
            return min(fg_a * bg_a, bg * (fg_a / (fg_a * bg_a - fg * bg_a)));
        

class Overlay(BlendMode):
    """
    Overlay blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        if bg * 2 > bg_a:
            return (
                self.comp(fg, bg_a) + self.comp(bg, fg_a) 
                - 2 * (bg_a - bg) * (fg_a - fg) + fg_a * bg_a
            )
        else:
            return fg * bg * 2 + self.comp(fg, bg_a) + self.comp(bg, fg_a)
        

class SoftLight(BlendMode):
    """
    Soft Light blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        fg_n = fg / fg_a

        if 2 * bg <= bg_a:
            return (
                fg * (bg_a + (2 * bg - bg_a) * (1 - fg_n))
                + self.comp(bg, fg_a) + self.comp(fg, bg_a)
            )
        elif 2 * bg > bg_a and 4 * fg <= fg_a:
            return (
                fg_a * (2 * bg - bg_a) * (16 * fg_n**3 - 12 * fg_n**2 - 3 * fg_n)
                + bg - bg * fg_a + fg
            )
        else:
            return fg_a * (2 * bg - bg_a) * (fg_n**0.5 - fg_n) + bg - bg * fg_a + fg


class HardLight(BlendMode):
    """
    Hard Light blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        if fg * 2 > fg_a:
            return (
                fg_a * bg_a - 2 * (bg_a - bg) * (fg_a - fg) 
                + self.comp(fg, bg_a) + self.comp(bg, fg_a)
            )
        else:
            return 2 * fg * bg + self.comp(fg, bg_a) + self.comp(bg, fg_a)
        
        
class Difference(BlendMode):
    """
    Difference blending mode.
    """

    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return fg + bg - 2 * min(fg * bg_a, bg * fg_a);


class Exclusion(BlendMode):
    """
    Exclusion blending mode.
    """
    
    def blend(self, bg: float, fg: float, bg_a: float, fg_a: float) -> float:
        return (
            (fg * bg_a + bg * fg_a - 2 * fg * bg) 
            + self.comp(fg, bg_a) + self.comp(bg, fg_a)
        )
    