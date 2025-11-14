# file: gui/tools/inspect_tool.py
from gui.tools.base_tool import BaseTool
from tkinter import messagebox

class InspectTool(BaseTool):
    name = "inspect"

    def on_click(self, coord, grid, widget):
        tile = grid.get(coord)
        messagebox.showinfo(
            "Hex Info",
            f"Coord: {coord}\nBiome: {tile.biome_id}\nTrails: {tile.trails}"
        )