class BlendMode:
    """
    Base class of blending modes.
    """

    def _alpha(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> float:
        return bg[3] + fg[3] * (1 - bg[3])
    
    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        """
        Blend normalized colors.

        Parameters
        ----------
        bg: `tuple[float, float, float, float]`
            Background RGBA tuple.
        fg: `tuple[float, float, float, float]`
            Foreground RGBA tuple.
        """
        raise NotImplementedError("Blend method is not implemented")
   
    def compose(self, bg, fg):
        """
        Compose background and foreground colors.

        Parameters
        ----------
        bg: `RGBA`
            Background color.
        fg: `RGBA`
            Foreground color.

        Raises
        ------
        `ValueError` 
            If bit counts of the colors do not match.
        """
        from .rgba import RGBA

        bg: RGBA = bg
        fg: RGBA = fg

        if bg.bits != fg.bits:
            raise ValueError(f"Cannot blend colors with different size")

        bits = bg.bits
        max_one = (1 << bits) - 1

        blended = self.blend(bg.normalize(), fg.normalize())

        return RGBA([round(i * max_one) for i in blended], bits=bits)
        

class Normal(BlendMode):
    """
    Normal blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        a = self._alpha(bg, fg)

        if a == 0:
            return 0, 0, 0, 0

        def _ch(num: int) -> float:
            return (fg[num] * fg[3] + bg[num] * bg[3] * (1 - fg[3])) / a

        return _ch(0), _ch(1), _ch(2), a
    

class Darken(BlendMode):
    """
    Darken blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        a = self._alpha(bg, fg)

        def _ch(num: int) -> float:
            return (
                min(
                    fg[num] * bg[3], 
                    bg[num] * fg[3]
                ) 
                + fg[num] * (1 - bg[3]) 
                + bg[num] * (1 - fg[3])
            ) / a
            
        return _ch(0), _ch(1), _ch(2), a
    

class Multiply(BlendMode):
    """
    Multiply blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            return fg[num] * bg[num] + fg[num] * (1 - bg[3]) + bg[num] * (1 - fg[3])
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
      

class ColorBurn(BlendMode):
    """
    Color burn blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            if fg[num] == 0:
                return bg[num] * (1 - fg[3])
            elif bg[num] == bg[3]:
                return fg[3] * bg[3] + bg[num] * (1 - fg[3])
            else:
                return (
                    bg[3] * fg[3] 
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3])
                    - min(
                        fg[3] * bg[3], 
                        ((bg[3] * fg[3] - bg[num] * fg[3]) / fg[num] * bg[3])
                    )
                )
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)


class Lighten(BlendMode):
    """
    Lighten blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            return (
                max(
                    fg[num] * bg[3],
                    bg[num] * fg[3]
                ) 
                + fg[num] * (1 - bg[3]) 
                + bg[num] * (1 - fg[3])
            )
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
    

class Screen(BlendMode):
    """
    Screen blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            return 1 - (1 - bg[num] * bg[3]) * (1 - fg[num] * fg[3])
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)


class ColorDodge(BlendMode):
    """
    Color dodge blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float: 
            if fg[num] == fg[3]:
                if bg[num] == 0:
                    return fg[num] * (1 - bg[3])
                else:
                    return fg[3] * bg[3] + fg[num] * (1 - bg[3]) + bg[num] * (1 - fg[3])
            else:
                denominator = fg[3] * bg[3] - fg[num] * bg[3]
                return (
                    fg[3] * bg[3]
                    if denominator == 0 
                    else min(
                        fg[3] * bg[3], 
                        bg[num] * (fg[3] / denominator)
                    )
                )

        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
        

class Overlay(BlendMode):
    """
    Overlay blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            if bg[num] * 2 > bg[3]:
                return (
                    fg[3] * bg[3]
                    - 2 * (bg[3] - bg[num]) * (fg[3] - fg[num]) 
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3]) 
                )
            else:
                return (
                    fg[num] * bg[num] * 2 
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3]) 
                )
            
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
        

class SoftLight(BlendMode):
    """
    Soft light blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            if fg[3] == 0:
                return bg[num]
            
            fg_n = fg[num] / fg[3]

            if 2 * bg[num] <= bg[3]:
                return (
                    fg[num] * (bg[3] + (2 * bg[num] - bg[3]) * (1 - fg_n))
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3]) 
                )
            elif 2 * bg[num] > bg[3] and 4 * fg[num] <= fg[3]:
                return (
                    fg[3] * (2 * bg[num] - bg[3]) 
                    * (16 * fg_n ** 3 - 12 * fg_n ** 2 - 3 * fg_n)
                    + bg[num] - bg[num] * fg[3] + fg[num]
                )
            else:
                return (
                    fg[3] * (2 * bg[num] - bg[3]) 
                    * (fg_n ** 0.5 - fg_n) 
                    + bg[num] - bg[num] * fg[3] + fg[num]
                )
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)


class HardLight(BlendMode):
    """
    Hard light blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            if fg[num] * 2 > fg[3]:
                return (
                    fg[3] * bg[3] - 2 * (bg[3] - bg[num]) * (fg[3] - fg[num]) 
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3]) 
                )
            else:
                return (
                    2 * fg[num] * bg[num]
                    + fg[num] * (1 - bg[3]) 
                    + bg[num] * (1 - fg[3]) 
                )
            
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
        
        
class Difference(BlendMode):
    """
    Difference blending mode.
    """

    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            return (
                fg[num] + bg[num] 
                - 2 * min(fg[num] * bg[3], bg[num] * fg[3])
            )
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
                

class Exclusion(BlendMode):
    """
    Exclusion blending mode.
    """
    
    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        def _ch(num: int) -> float:
            return (
                fg[num] * bg[3] 
                + bg[num] * fg[3] 
                - 2 * fg[num] * bg[num]
                + fg[num] * (1 - bg[3]) 
                + bg[num] * (1 - fg[3]) 
            )
        
        return _ch(0), _ch(1), _ch(2), self._alpha(bg, fg)
    