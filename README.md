# pinkie
[![pypi](https://img.shields.io/pypi/v/pinkie)](https://pypi.org/project/pinkie) [![python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/downloads) [![python](https://img.shields.io/badge/support-yellow)](https://www.buymeacoffee.com/eeemoon)

All-in-one solution for color management.

## Features
- Simple and pythonic way to manage colors
- Multiple models (`RGB`, `HSL`, `CMYK`, `HEX`) and conversions
- Palettes, schemes and color generators
- Color blending with many modes
- Supports alpha (transparency) channel

## Installation
To install this package, run the following command:
```
pip install pinkie
```

## Usage
### Get started
You can define colors like below. `Color` equals `RGBA` color.
```python
from pinkie import Color

color = Color('c0ffee') 
```

### Initialize colors
You can create colors in different ways:
```python
Color((244, 11, 58)) # rgb tuple, alpha is set to 255
Color((244, 11, 58, 215)) # rgba tuple
Color('#ff53a7') # hex value ('#' is automatically stripped)
Color('ff53a7f6') # hex value with alpha
Color(43252667) # int value
HSLA((259, 94, 47)).to_rgba() # hsl value
...
```
and define colors with another bit count per channel:
```python
Color((34832, 632, 65103), bits=16) # rgb tuple
Color('ff53a7cc671a', bits=16) # hex value
Color('ff53a7cc671a12e3', bits=16) # hex value with alpha
...
```

### Color conversions
Color models can be converted to `RGBA` and back:
```python
Color('ff00ff').to_hsla() 
Color('157cc3').to_cmyk()
HSLA('44c26b').to_rgba()
...
```

### Color blending
You can blend colors like in Photoshop:
```python
import pinkie.blend as blend
from pinkie import Color

bg = Color('ffd015ff')
fg = Color('ff15bd80')

bg.blend(fg, blend.Normal()) # FF7269FF
```
and create your own blending mode:
```python
class MyBlend(BlendMode):
    def blend(
        self, 
        bg: tuple[float, float, float, float], 
        fg: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        a = self._alpha(bg, fg)

        def _ch(num: int) -> float:
            return bg[num] * fg[num]

        return _ch(0), _ch(1), _ch(2), a

bg.blend(fg, MyBlend())
```

### Harmonic colors
There are various methods to get harmonic colors:
```python
color.complementary() # complementary color
color.triadic() # list of triadic colors
color.closest(Color('ffffff'), Color('000000')) # closest color from the list
...
```

### Color palettes
Palettes are just sequences of colors. You can manage them like this:
```python
from pinkie import Color, Palette

palette = Palette(Color('ffffff'), Color('4c66a1'))
palette.add(Color('16c235'))
palette.remove(Color('ffffff'))

Palette.web() # palette of web-safe colors
Palette.gradient(Color('ff0000'), Color('0000ff'), 5) # palette of colors that create gradient from red to blue
...
```