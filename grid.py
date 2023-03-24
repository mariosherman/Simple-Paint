from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_util import *
from layer_store import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.draw_style = draw_style
        if self.draw_style == self.DRAW_STYLE_OPTIONS[0]:
            layer_store_type = SetLayerStore
        elif self.draw_style == self.DRAW_STYLE_OPTIONS[1]:
            layer_store_type = AdditiveLayerStore
        elif self.draw_style == self.DRAW_STYLE_OPTIONS[2]:
            layer_store_type = SequenceLayerStore
        self.grid = ArrayR(x)
        for i in range(len(self.grid)):
            self.grid[i] = ArrayR(y)
            for j in range(len(self.grid[i])):
                self.grid[i][j] = layer_store_type()
        self.brush_size = self.DEFAULT_BRUSH_SIZE

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                self.grid[x][y].special()
    
    def __getitem__ (self, x: int):
        return self.grid[x]

if __name__ == "__main__":
    g = Grid('a', 2,4)
    # g.increase_brush_size()
    # g.increase_brush_size()
    # g.increase_brush_size()
    # g.increase_brush_size()
    # print(g.brush_size)