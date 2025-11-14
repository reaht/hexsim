# file: gui/input/tool_dispatch.py

class ToolDispatch:
    """
    Central routing of UI mouse events → tools.
    This version correctly:
      - Receives Tk events
      - Converts pixel → hex coords
      - Dispatches to the active tool
    """

    def __init__(self, state):
        self.state = state
        self.grid_widget = None  # MUST be attached by controller

    def attach_widget(self, widget):
        self.grid_widget = widget

    # ---------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------

    def on_click(self, event):
        """Mouse press → tool.on_click(coord, state)."""
        if not self.grid_widget:
            return

        coord = self.grid_widget.pixel_to_hex(event.x, event.y)
        if coord not in self.state.grid.tiles:
            return

        tool = self.state.tools[self.state.current_tool_var.get()]
        tool.on_click(coord, self.state)

    def on_drag(self, event):
        """Mouse drag → tool.on_drag(coord, state)."""
        if not self.grid_widget:
            return

        coord = self.grid_widget.pixel_to_hex(event.x, event.y)
        if coord not in self.state.grid.tiles:
            return

        tool = self.state.tools[self.state.current_tool_var.get()]
        tool.on_drag(coord, self.state)

    def on_release(self, event):
        """Mouse release → tool.on_release(state)."""
        tool = self.state.tools[self.state.current_tool_var.get()]
        tool.on_release(self.state)