# file: gui/renderers/layers/trail_layer.py
from gui.renderers.layers.base_layer import BaseRenderLayer
from core.grid import HexGrid
from core.movement import AXIAL_DIRECTIONS
import tkinter as tk


class TrailLayer(BaseRenderLayer):

    def draw(self, grid: HexGrid, _party_positions):
        if not self.enabled:
            return

        s = self.hex_math.s

        for (q, r), tile in grid.tiles.items():
            cx, cy = self.hex_math.axial_to_pixel(q, r)
            trails = tile.trails
            if not trails:
                continue

            for dir_index, exists in enumerate(trails):
                if not exists:
                    continue

                dq, dr = AXIAL_DIRECTIONS[dir_index]
                dx, dy = self.hex_math.axial_to_pixel_raw(dq, dr)

                x2 = cx + dx * 0.4
                y2 = cy + dy * 0.4

                self.canvas.create_line(
                    cx, cy, x2, y2,
                    width=4, fill="brown", capstyle="round"
                )