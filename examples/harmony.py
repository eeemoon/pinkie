from pinkie import Color


color = Color('ff526c')

# color schemes
print("Complementary:", color.complementary().hex)
print("Split complementary:", *(i.hex for i in color.split_complementary()))
print("Triadic:", *(i.hex for i in color.triadic()))
print("Tetradic:", *(i.hex for i in color.tetradic()))
print("Analogous:", *(i.hex for i in color.analogous()))

# other methods
print("Closest:", color.closest([Color('4fc10a'), Color('bb57a2')]).hex)