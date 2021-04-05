#!/usr/bin/env python3

# Dimetric grid generator
# screenshot: https://i.imgur.com/HxSRk4C.png
# dep: [Pillow](https://pypi.org/project/Pillow/)

import typing as t
import collections
from PIL import Image, ImageDraw # type: ignore
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Segment:
    width:int; height:int; n:int

class Edge:
    def __init__(self, seg:Segment):
        """An edge is one side of a rhombus. It is composed of n segments. Each
        segment is a rectangle of width*height pixels."""
        self.seg = seg

    def width(self):
        return self.seg.n * self.seg.width

    def height(self):
        return self.seg.n * self.seg.height

    def size(self):
        return (self.width(), self.height())

    def image(self, fgcolor:str, bgcolor:str):
        img = Image.new('RGBA', self.size(), bgcolor)
        drawtool = ImageDraw.Draw(img)

        for i in range(self.seg.n):
            x = self.width() - (i + 1) * self.seg.width
            y = self.seg.height * i
            p1 = (x, y)
            p2 = (x + self.seg.width - 1, y + self.seg.height - 1)
            drawtool.rectangle((p1, p2), fgcolor)

        return img

    def __str__(self):
        return f"e{self.seg.width}x{self.seg.height}x{self.seg.n}"

class Tile:
    def __init__(self, edge:Edge):
        """A Tile is composed of an edge mirrored vertically and horizontally to
        form a rhombus."""
        self.edge = edge

    def width(self):
        return 2 * self.edge.width()

    def height(self):
        return 2 * self.edge.height()

    def size(self):
        return [self.width(), self.height()]

    def image(self, fgcolor:str, bgcolor:str):
        img = Image.new('RGBA', self.size())
        img.paste(self.edge.image(fgcolor, bgcolor), (0, 0))
        img.alpha_composite(img.transpose(Image.FLIP_LEFT_RIGHT))
        img.alpha_composite(img.transpose(Image.FLIP_TOP_BOTTOM))
        return img

    def __str__(self):
        return f"t{self.width()}x{self.height()}_{self.edge}"

class Grid:
    def __init__(self, tile:Tile, n:t.Tuple[int, int]):
        """A Grid is composed of n*n tiles."""
        self.tile = tile
        self.n = n

    def width(self):
        return self.n[0] * self.tile.width()

    def height(self):
        return self.n[1] * self.tile.height()

    def size(self):
        return [self.width(), self.height()]

    def image(self, fgcolor:str, bgcolor:str):
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
        tile = Tile(Edge(Segment(width=4, height=2, n=8))),
        n = (10, 10)
    )
    save(grid)
