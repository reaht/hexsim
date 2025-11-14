# file: gui/tools/paint_trail_tool.py
from typing import Tuple, Optional

from gui.tools.base_tool import BaseTool
from gui.app_state import AppState
from core.movement import AXIAL_DIRECTIONS

Coord = Tuple[int, int]


class PaintTrailTool(BaseTool):
    name = "paint_trail"

    def __init__(self):
        self.last_coord: Optional[Coord] = None

    def on_click(self, coord: Coord, state: AppState):
        # Start of a stroke: remember starting hex, no trail yet
        if coord not in state.grid.tiles:
            return
        self.last_coord = coord

    def on_drag(self, coord: Coord, state: AppState):
        if coord not in state.grid.tiles:
            return

        if self.last_coord is None:
            self.last_coord = coord
            return

        if coord == self.last_coord:
            return

        dq = coord[0] - self.last_coord[0]
        dr = coord[1] - self.last_coord[1]

        dir_idx = None
        for i, (adq, adr) in enumerate(AXIAL_DIRECTIONS):
            if (adq, adr) == (dq, dr):
                dir_idx = i
                break

        if dir_idx is None:
            # non-adjacent; reset stroke
            self.last_coord = coord
            return

        # Bidirectional trail
        state.grid.set_trail(self.last_coord, dir_idx, True)

        self.last_coord = coord
        state.events.publish("grid_changed")

    def on_release(self, state: AppState):
        self.last_coord = None