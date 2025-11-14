# file: gui/tools/pain t_biome_tool.py
from typing import Tuple
import tkinter as tk

from gui.tools.base_tool import BaseTool
from gui.app_state import AppState

Coord = Tuple[int, int]


class PaintBiomeTool(BaseTool):
    name = "paint_biome"

    def __init__(self, biome_var: tk.StringVar):
        self.biome_var = biome_var

    def on_click(self, coord: Coord, state: AppState):
        if coord not in state.grid.tiles:
            return

        biome_id = self.biome_var.get()
        state.grid.set_biome(coord, biome_id)
        state.events.publish("grid_changed")

    def on_drag(self, coord: Coord, state: AppState):
        # allow drag painting
        self.on_click(coord, state)