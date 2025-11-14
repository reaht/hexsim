# file: gui/renderers/layers/gridline_layer.py
import math
from gui.renderers.layers.base_layer import BaseRenderLayer


class GridlineLayer(BaseRenderLayer):

    def draw(self, grid, _party):
        if not self.enabled:
            return

        s = self.hex_math.s

        for (q, r) in grid.tiles:
            cx, cy = self.hex_math.axial_to_pixel(q, r)

            pts = []
            for i in range(6):
                angle = math.radians(60 * i)
                pts.append(cx + s * math.cos(angle))
                pts.append(cy + s * math.sin(angle))

            self.canvas.create_polygon(pts, fill="", outline="#666", width=1)