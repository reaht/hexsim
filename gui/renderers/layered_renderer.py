# file: gui/renderers/layered_renderer.py
from typing import List
from gui.renderers.layers.base_layer import BaseRenderLayer
from core.grid import HexGrid


class LayeredRenderer:
    """
    Owns multiple rendering layers and draws them in order.
    Each layer draws only its own elements and does not clear the canvas.
    """

    def __init__(self, canvas, layers: List[BaseRenderLayer]):
        self.canvas = canvas
        self.layers = layers

    def draw(self, grid: HexGrid, party_positions):
        # Clear once
        self.canvas.delete("all")

        # Draw in layer order
        for layer in self.layers:
            if layer.enabled:
                layer.draw(grid, party_positions)