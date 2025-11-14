# file: gui/renderers/layers/party_layer.py
from gui.renderers.layers.base_layer import BaseRenderLayer
from typing import List, Tuple
import tkinter as tk


class PartyLayer(BaseRenderLayer):

    def draw(self, grid, party_positions: List[Tuple[int, int]]):
        if not self.enabled:
            return

        s = self.hex_math.s

        for (q, r) in party_positions:
            cx, cy = self.hex_math.axial_to_pixel(q, r)
            r0 = s * 0.35
            self.canvas.create_oval(
                cx - r0, cy - r0,
                cx + r0, cy + r0,
                fill="red", outline="black", width=2
            )