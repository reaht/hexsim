# file: gui/tools/pain_trail_tool.py

from core.movement import AXIAL_DIRECTIONS
from core.command import SetTrailCommand

class PaintTrailTool:
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

        # Must be a valid neighbor direction
        direction = None
        for i, (aq, ar) in enumerate(AXIAL_DIRECTIONS):
            if (aq, ar) == (dq, dr):
                direction = i
                break

        if direction is None:
            self.last = coord
            return

        old = state.grid.get(self.last).trails[direction]
        if old is True:
            self.last = coord
            return

        cmd = SetTrailCommand(self.last, direction, old, True)
        state.undo.add(cmd)

        self.last = coord

    def on_release(self, state):
        state.undo.commit(state)
        self.last = None