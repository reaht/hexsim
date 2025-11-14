# file: gui/tools/paint_trail_tool.py

from core.movement import AXIAL_DIRECTIONS
from core.command import SetTrailCommand

class PaintTrailTool:
    """
    Drag to paint trails. Automatically snaps drag movements to the
    nearest axial direction, so painting always works even with
    imperfect mouse movement.
    """

    def __init__(self):
        self.last = None

    def on_click(self, coord, state):
        self.last = coord
        state.undo.begin()

    def on_drag(self, coord, state):
        print("drag:", coord, "last:", self.last)
        if self.last is None or coord == self.last:
            return

        dq = coord[0] - self.last[0]
        dr = coord[1] - self.last[1]

        # Snap drag vector to nearest direction
        direction = self._closest_direction(dq, dr)
        if direction is None:
            self.last = coord
            return

        tile = state.grid.get(self.last)
        old = tile.trails[direction]

        # Already painted → nothing to do
        if old is True:
            self.last = coord
            return

        cmd = SetTrailCommand(self.last, direction, old, True)
        state.undo.add(cmd)

        self.last = coord

    def on_release(self, state):
        state.undo.commit(state)
        self.last = None

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _closest_direction(self, dq, dr):
        best = 999999
        best_dir = None

        for i, (aq, ar) in enumerate(AXIAL_DIRECTIONS):
            dist = abs(dq - aq) + abs(dr - ar)
            if dist < best:
                best = dist
                best_dir = i

        # Reject large mismatches (diagonal drags, jitter)
        return best_dir if best <= 1 else None