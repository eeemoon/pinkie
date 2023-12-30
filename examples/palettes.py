from pinkie import Color, Palette


# basic palette management
palette = Palette([Color('ffffff'), Color('4c66a1')])
palette.add(Color('16c235'))
palette.remove(Color('ffffff'))

# palette generators
Palette.web()
Palette.random(7)

# gradient palette
start = Color('ff0000')
end =  Color('0000ff')
gradient = Palette.gradient(start, end, 5)

print(f"Gradient from {start.hex} to {end.hex}:")
for i in gradient:
    print(i.hex)