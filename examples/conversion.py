from pinkie import Color


color = Color('44c71a')

# available conversions
print("RGBA:", color)
print("HSLA:", color.to_hsla())
print("CMYK:", color.to_cmyk())
print("Web:", color.to_web())