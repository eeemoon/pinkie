from pinkie import Color, Palette


color = Color('44c71a')


# other color models
print("RGBA:", color)
print("HSLA:", color.to_hsla())
print("CMYK:", color.to_cmyk())


# advanced
web_color = color.closest(*Palette.web())
print("Web:", web_color)