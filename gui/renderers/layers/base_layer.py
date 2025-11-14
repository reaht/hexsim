# file: gui/renderers/layers/base_layer.py
from typing import Optional, List, Tuple
from core.grid import HexGrid
from core.hex_math import HexMath
import tkinter as tk

Coord = Tuple[int, int]


class BaseRenderLayer:
    """
    Abstract base class for all rendering layers.
    Each layer receives a canvas and hex_math and draws *only* its own content.
    """

    def __init__(self, canvas: tk.Canvas, hex_math: HexMath):
        self.canvas = canvas
        self.hex_math = hex_math
        self.enabled = True

    def draw(self, grid: HexGrid, party_positions: List[Coord]):
        """
        Override in subclasses. Should not delete the canvas.
        Should only draw its own elements.
        """
        pass