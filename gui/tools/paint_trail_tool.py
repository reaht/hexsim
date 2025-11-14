# file: gui/tools/paint_trail_tool.py
from gui.tools.base_tool import BaseTool
from core.movement import AXIAL_DIRECTIONS

class PaintTrailTool(BaseTool):
    name = "paint_trail"

    def __init__(self):
        self.last_coord = None

    def on_click(self, coord, grid, widget):
        self.last_coord = coord

    def on_drag(self, coord, grid, widget):
        if self.last_coord is None:
            self.last_coord = coord
            return

        if coord == self.last_coord:
            return

        # Compute dq/dr movement
        dq = coord[0] - self.last_coord[0]
        dr = coord[1] - self.last_coord[1]

        # Find direction index
        for i, (adq, adr) in enumerate(AXIAL_DIRECTIONS):
            if (dq, dr) == (adq, adr):
                grid.set_trail(self.last_coord, i, True)
                break

        self.last_coord = coord
        widget.redraw()

    def on_release(self, grid, widget):
        self.last_coord = None