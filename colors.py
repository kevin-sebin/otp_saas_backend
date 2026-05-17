import random

dark_colors = [
    "#1f2937",  # slate charcoal
    "#2b2d42",  # muted indigo
    "#3d405b",  # dusty navy
    "#2d1e2f",  # dark plum
    "#432818",  # mocha brown
    "#3c1518",  # espresso
    "#4a2c2a",  # cocoa
    "#540b0e",  # oxblood
    "#3f0d12",  # deep wine
    "#240046",  # midnight purple
    "#10002b",  # black violet
    "#252422",  # ash black
    "#22333b",  # smoky teal
    "#283618",  # dark olive
    "#1b4332",  # forest emerald
]

def selColor(arr):
    col = random.choices(arr)
    return col[0]
