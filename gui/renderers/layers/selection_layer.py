# file: gui/renderers/layers/selection_layer.py
import math
from typing import Optional, Tuple, List
import tkinter as tk

from gui.renderers.layers.base_layer import BaseRenderLayer

Coord = Tuple[int, int]


class SelectionLayer(BaseRenderLayer):
    """
    Draws outlines for:
      - hovered hex (yellow)
      - selected hex (cyan)
    """

    def __init__(self, canvas: tk.Canvas, hex_math, outline_width=3):
        super().__init__(canvas, hex_math)
        self.hovered: Optional[Coord] = None
        self.selected: Optional[Coord] = None
        self.outline_width = outline_width

    def set_hovered(self, coord: Optional[Coord]):
        self.hovered = coord

    def set_selected(self, coord: Optional[Coord]):
        self.selected = coord

    def draw(self, grid, _party_positions):
        if not self.enabled:
            return

        s = self.hex_math.s

        # Draw selected
        if self.selected in grid.tiles:
            self._draw_outline(self.selected, "#00ffff", self.outline_width)

        # Draw hovered (only if different)
        if self.hovered in grid.tiles and self.hovered != self.selected:
            self._draw_outline(self.hovered, "#ffff00", self.outline_width)

    # ---------------------------------------------------------
    # Internal outline drawing
    # ---------------------------------------------------------

    def _draw_outline(self, coord: Coord, color: str, width: int):
        q, r = coord
        cx, cy = self.hex_math.axial_to_pixel(q, r)
        s = self.hex_math.s

        pts = []
        for i in range(6):
            angle = math.radians(60 * i)
            pts.append(cx + s * math.cos(angle))
            pts.append(cy + s * math.sin(angle))

        self.canvas.create_polygon(
            pts,
            fill="",
            outline=color,
            width=width
        )