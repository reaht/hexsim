# file: gui/tools/erase_trail_tool.py

from core.movement import AXIAL_DIRECTIONS
from core.command import SetTrailCommand

class EraseTrailTool:
    """
    Drag to remove trails. Identical behaviour to PaintTrailTool,
    except it sets trail=False instead of True.
    """

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

        direction = self._closest_direction(dq, dr)
        if direction is None:
            self.last = coord
            return

        tile = state.grid.get(self.last)
        old = tile.trails[direction]

        # Already erased → nothing to do
        if old is False:
            self.last = coord
            return

        cmd = SetTrailCommand(self.last, direction, old, False)
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

        return best_dir if best <= 1 else None