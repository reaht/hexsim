# file: gui/tools/erase_trail_tool.py
from gui.tools.base_tool import BaseTool
from core.movement import AXIAL_DIRECTIONS

class EraseTrailTool(BaseTool):
    name = "erase_trail"

    def __init__(self):
        self.last_coord = None

    def on_click(self, coord, grid, widget):
        """
        First click marks starting point. No deletion occurs yet,
        because erasing only happens when crossing into an adjacent hex.
        """
        self.last_coord = coord

    def on_drag(self, coord, grid, widget):
        if self.last_coord is None:
            self.last_coord = coord
            return

        if coord == self.last_coord:
            return

        dq = coord[0] - self.last_coord[0]
        dr = coord[1] - self.last_coord[1]

        # Find direction from last_coord -> coord
        dir_idx = None
        for i, (adq, adr) in enumerate(AXIAL_DIRECTIONS):
            if (adq, adr) == (dq, dr):
                dir_idx = i
                break

        if dir_idx is None:
            # Dragged to a non-adjacent hex → reset stroke
            self.last_coord = coord
            return

        # Remove trail on the starting hex
        grid.set_trail(self.last_coord, dir_idx, False)

        # Remove mirrored trail on the neighbour, if it exists
        rev_idx = (dir_idx + 3) % 6
        if coord in grid.tiles:
            grid.set_trail(coord, rev_idx, False)

        self.last_coord = coord
        widget.redraw()

    def on_release(self, grid, widget):
        self.last_coord = None