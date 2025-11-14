# file: gui/renderers/layers/tile_layer.py
import math
import tkinter as tk
from gui.renderers.layers.base_layer import BaseRenderLayer
from core.grid import HexGrid


class TileLayer(BaseRenderLayer):
    """
    Hex tile background renderer.
    Biome color comes directly from:
        grid.biome_lib.get(tile.biome_id).color
    """

    def __init__(self, canvas: tk.Canvas, hex_math, biome_colors=None):
        """
        `biome_colors` is now unused but kept for backward compatibility.
        """
        super().__init__(canvas, hex_math)
        self.biome_colors = biome_colors or {}

    def draw(self, grid: HexGrid, _party_positions):
        if not self.enabled:
            return

        s = self.hex_math.s
        biome_lib = grid.biome_lib

        for (q, r), tile in grid.tiles.items():
            cx, cy = self.hex_math.axial_to_pixel(q, r)

            # -----------------------------------------------------
            # Get biome → color
            # -----------------------------------------------------
            biome = biome_lib.get(tile.biome_id)

            # fallback if CSV entry missing or color empty
            fill = getattr(biome, "color", None) or "#cccccc"

            # -----------------------------------------------------
            # Compute hex points
            # -----------------------------------------------------
            pts = []
            for i in range(6):
                angle = math.radians(60 * i)
                pts.append(cx + s * math.cos(angle))
                pts.append(cy + s * math.sin(angle))

            # -----------------------------------------------------
            # Draw polygon
            # -----------------------------------------------------
            self.canvas.create_polygon(
                pts,
                fill=fill,
                outline="black",
                width=1
            )