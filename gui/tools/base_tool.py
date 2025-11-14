# file: gui/tools/base_tool.py

class BaseTool:
    """Interface for map-editing tools."""

    name = "base"

    def on_click(self, coord, grid, widget):
        pass

    def on_drag(self, coord, grid, widget):
        pass

    def on_release(self, grid, widget):
        pass