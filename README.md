# pinkie
[![pypi](https://img.shields.io/pypi/v/pinkie)](https://pypi.org/project/pinkie) [![python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/downloads) [![python](https://img.shields.io/badge/support-yellow)](https://www.buymeacoffee.com/eeemoon)

All-in-one solution for color management.

## Features
- Simple pythonic way to manage colors
- Multiple models (RGB, HSL, HEX) and conversions
- Palettes and schemes and color generators
- Many blending modes
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
HSLA(259, 94, 47).to_rgba() # hsl value
# etc
```
and define colors with another bit count for channel
```python
Color((34832, 632, 65103)) # rgb tuple
Color('ff53a7cc671a', bits=16) # hex value
Color('ff53a7cc671a12e3', bits=16) # hex value with alpha
# etc
```

### Color representation
Color values can be accessed like this:
```python
color.rgba # rgba tuple
color.rgb # rgb tuple
color.hex # hex value
color.red # red value
color.r # also red value
# etc
```

### Color blending
You can blend colors like in Photoshop
```python
import pinkie.blend as blend
from pinkie import Color

bg = Color('ffd015ff')
fg = Color('ff15bd80')

bg.blend(fg, blend.Normal) # FF7269FF
```
and create your own blending mode:
```python
class MyBlend(blend.BlendMode):
    """
    Blend mode that always return white.
    """
    def blend(self, bg, fg):
        # specifying 'bits' is important if you want
        # to blend mode work correctly with any color
        return Color('ffffff', bits=self.bits)

bg.blend(fg, MyBlend)
```

### Linked colors
There are various methods to get nice-looking colors
```python
color.complementary() # complementary color
color.split_complementary() # 2 split complementary colors
color.closest([Color('ffffff'), Color('000000')]) # closest color from the list
```