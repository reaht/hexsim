# file: gui/tools/inspect_tool.py
from typing import Tuple
from tkinter import messagebox

from gui.tools.base_tool import BaseTool
from gui.app_state import AppState

Coord = Tuple[int, int]


class InspectTool(BaseTool):
    name = "inspect"

    def on_click(self, coord: Coord, state: AppState):
        tile = state.grid.get(coord)
        if tile is None:
            messagebox.showinfo("Hex Info", f"Coord: {coord}\n(No tile)")
            return

        messagebox.showinfo(
            "Hex Info",
            f"Coord: {coord}\nBiome: {tile.biome_id}\nTrails: {tile.trails}",
        )