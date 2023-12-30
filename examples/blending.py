import pinkie.blend as blend
from pinkie import Color


# background and foreground colors for blending
bg = Color('55f6a380')
fg = Color('ffb15780')

# available blend modes
modes = [
    blend.Normal,
    blend.Darken,
    blend.Multiply,
    blend.ColorBurn,
    blend.Lighten,
    blend.Screen,
    blend.ColorDodge,
    blend.Overlay,
    blend.SoftLight,
    blend.HardLight,
    blend.Difference,
    blend.Exclusion,
]

for mode in modes:
    color = bg.blend(fg, mode)

    print(mode.__name__, "-", color.hexa)