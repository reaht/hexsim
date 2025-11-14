# file: gui/tools/paint_biome_tool.py

from core.command import ChangeBiomeCommand

class PaintBiomeTool:
    def __init__(self, biome_var):
        self.biome_var = biome_var

    def on_click(self, coord, state):
        old = state.grid.get(coord).biome_id
        new = self.biome_var.get()

        cmd = ChangeBiomeCommand(coord, old, new)
        state.undo.do(cmd, state)

    def on_drag(self, coord, state):
        old = state.grid.get(coord).biome_id
        new = self.biome_var.get()

        if old == new:
            return

        cmd = ChangeBiomeCommand(coord, old, new)
        state.undo.do(cmd, state)

    def on_release(self, state):
        pass