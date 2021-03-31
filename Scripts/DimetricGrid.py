#!/usr/bin/env python3

# Dimetric grid generator
# screenshot: https://i.imgur.com/HxSRk4C.png
# dep: [Pillow](https://pypi.org/project/Pillow/)

import collections
from PIL import Image, ImageDraw
from pathlib import Path

class Edge:
    def __init__(self, segwidth, segheight, segn):
        self.segwidth = segwidth
        self.segheight = segheight
        self.segn = segn

    def width(self):
        return self.segn * self.segwidth

    def height(self):
        return self.segn * self.segheight

    def size(self):
        return (self.width(), self.height())

    def image(self, fgcolor, bgcolor):
        img = Image.new('RGBA', self.size(), bgcolor)
        drawtool = ImageDraw.Draw(img)

        for i in range(self.segn):
            x = self.width() - (i + 1) * self.segwidth
            y = self.segheight * i
            p1 = (x, y)
            p2 = (x + self.segwidth - 1, y + self.segheight - 1)
            drawtool.rectangle((p1, p2), fgcolor)

        return img

    def __str__(self):
        return f"e{self.segwidth}x{self.segheight}x{self.segn}"

class Tile:
    def __init__(self, edge):
        self.edge = edge

    def width(self):
        return 2 * self.edge.width()

    def height(self):
        return 2 * self.edge.height()

    def size(self):
        return [self.width(), self.height()]

    def image(self, fgcolor, bgcolor):
        img = Image.new('RGBA', self.size())
        img.paste(self.edge.image(fgcolor, bgcolor), (0, 0))
        img.alpha_composite(img.transpose(Image.FLIP_LEFT_RIGHT))
        img.alpha_composite(img.transpose(Image.FLIP_TOP_BOTTOM))
        return img

    def __str__(self):
        return f"t{self.width()}x{self.height()}_{self.edge}"

class Grid:
    def __init__(self, tile, n):
        self.tile = tile
        self.n = n

    def width(self):
        return self.n[0] * self.tile.width()

    def height(self):
        return self.n[1] * self.tile.height()

    def size(self):
        return [self.width(), self.height()]

    def image(self, fgcolor, bgcolor):
        tileimg = self.tile.image(fgcolor, bgcolor)
        gridimg = Image.new('RGBA', self.size())
        for x in range(0, self.width(), self.tile.width()):
            for y in range(0, self.height(), self.tile.height()):
                gridimg.paste(tileimg, (x, y))
        return gridimg

    def __str__(self):
        return f"g{self.width()}x{self.height()}_{self.tile}"

def save(element):
    filename = Path('out') / f"{element}.png"
    filename.parent.mkdir(exist_ok=True)
    element.image(fgcolor="#4B5263", bgcolor="#ABB2BF") \
           .save(filename)

if __name__ == "__main__":
    grid = Grid(
        tile = Tile(Edge(segwidth=4, segheight=2, segn=8)),
        n = (10, 10)
    )
    save(grid)
