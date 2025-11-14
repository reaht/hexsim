# file: gui/tools/erase_trail_tool.py
from core.movement import AXIAL_DIRECTIONS
from core.command import SetTrailCommand


class EraseTrailTool:
    def __init__(self):
        self.last = None

    def on_click(self, coord, state):
        self.last = coord
        state.undo.begin()

    def on_drag(self, coord, state):
        if self.last is None or coord == self.last:
            return

        dq = coord[0] - self.last[0]
        dr = coord[1] - self.last[1]

        direction = None
        for i, (aq, ar) in enumerate(AXIAL_DIRECTIONS):
            if (aq, ar) == (dq, dr):
                direction = i
                break
        if direction is None:
            self.last = coord
            return

        tile = state.grid.get(self.last)
        old = tile.trails[direction]
        new = "none"

        if old == new:
            self.last = coord
            return

        cmd = SetTrailCommand(self.last, direction, old, new)
        state.undo.add(cmd)

        self.last = coord

    def on_release(self, state):
        state.undo.commit(state)
        self.last = None