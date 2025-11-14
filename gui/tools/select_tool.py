# file: gui/tools/select_tool.py

from core.command import MovePartyCommand

class SelectTool:
    def on_click(self, coord, state):
        old = state.party.position
        new = coord

        if old == new:
            return

        cmd = MovePartyCommand(old, new)
        state.undo.do(cmd, state)

    def on_drag(self, coord, state):
        pass

    def on_release(self, state):
        pass