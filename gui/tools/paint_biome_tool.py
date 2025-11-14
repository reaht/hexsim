# file: gui/tools/paint_biome_tool.py
from gui.tools.base_tool import BaseTool

class PaintBiomeTool(BaseTool):
    name = "paint_biome"

    def __init__(self, biome_var):
        self.biome_var = biome_var

    def on_click(self, coord, grid, widget):
        grid.set_biome(coord, self.biome_var.get())
        widget.redraw()

    def on_drag(self, coord, grid, widget):
        self.on_click(coord, grid, widget)
