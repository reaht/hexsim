# file: gui/renderers/layers/trail_layer.py
from gui.renderers.layers.base_layer import BaseRenderLayer
from core.movement import AXIAL_DIRECTIONS
import tkinter as tk


class TrailLayer(BaseRenderLayer):
    def draw(self, grid, _party):
        if not self.enabled:
            return

        trail_lib = grid.trail_lib
        s = self.hex_math.s

        for (q, r), tile in grid.tiles.items():
            cx, cy = self.hex_math.axial_to_pixel(q, r)

            for dir_index, trail_id in enumerate(tile.trails):
                if trail_id == "none":
                    continue

                tt = trail_lib.get(trail_id)

                dq, dr = AXIAL_DIRECTIONS[dir_index]
                dx, dy = self.hex_math.axial_to_pixel_raw(dq, dr)

                x2 = cx + dx * 0.4
                y2 = cy + dy * 0.4

                self.canvas.create_line(
                    cx, cy, x2, y2,
                    width=tt.width,
                    fill=tt.color,
                    capstyle="round"
                )