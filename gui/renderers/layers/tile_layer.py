# file: gui/renderers/layers/tile_layer.py
import math
import tkinter as tk
from typing import Dict
from gui.renderers.layers.base_layer import BaseRenderLayer
from core.grid import HexGrid


class TileLayer(BaseRenderLayer):

    def __init__(self, canvas: tk.Canvas, hex_math, biome_colors: Dict[str, str]):
        super().__init__(canvas, hex_math)
        self.biome_colors = biome_colors

    def set_biome_colors(self, mapping):
        self.biome_colors = mapping

    def draw(self, grid: HexGrid, _party_positions):
        if not self.enabled:
            return

        s = self.hex_math.s

        for (q, r), tile in grid.tiles.items():
            cx, cy = self.hex_math.axial_to_pixel(q, r)
            fill = self.biome_colors.get(tile.biome_id, "#cccccc")

            pts = []
            for i in range(6):
                angle = math.radians(60 * i)
                pts.append(cx + s * math.cos(angle))
                pts.append(cy + s * math.sin(angle))

            self.canvas.create_polygon(pts, fill=fill, outline="black", width=1)