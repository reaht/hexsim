# file: gui/tools/select_tool.py
from gui.tools.base_tool import BaseTool

class SelectTool(BaseTool):
    name = "select"

    def on_click(self, coord, grid, widget):
        # Move party if widget tracks it
        if widget.party_positions:
            widget.party_positions[0] = coord
            widget.redraw()