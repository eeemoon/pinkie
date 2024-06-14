from pinkie import Color


color = Color('ff526c')


# color schemes
print("Complementary:", color.complementary())
print("Split complementary:", *color.split_complementary())
print("Triadic:", *color.triadic())
print("Tetradic:", *color.tetradic())
print("Analogous:", *color.analogous())


# other methods
print("Closest:", color.closest(Color('4fc10a'), Color('bb57a2')))
print("Furthest:", color.furthest(Color('4fc10a'), Color('bb57a2')))