#!/usr/bin/env python3

import argparse, random
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description='Create random pattern from the given images.')
parser.add_argument('n', type=int)
parser.add_argument('off', type=int)
parser.add_argument('paths', type=Path, nargs='+')
parser.add_argument('-o', '--out', type=Path, default='out/Pattern.png')
args = parser.parse_args()

symbols = list(Image.open(path) for path in args.paths)
# assumption: all the symbols have the same width and height
for sym in symbols[1:]:
    assert symbols[0].width == sym.width
    assert symbols[0].height == sym.height
width = (args.n * symbols[0].width) + (args.n - 1) * args.off
height = (args.n * symbols[0].height) + (args.n - 1) * args.off
output = Image.new('RGBA', (width, height))

for col in range(args.n):
    x = (col * symbols[0].width) + (col * args.off)
    for line in range(args.n):
        y = (line * symbols[0].height) + (line * args.off)
        symbol = random.choice(symbols)
        output.paste(symbol, (x, y))

output.save(args.out)
