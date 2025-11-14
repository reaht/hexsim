# file: gui/windows/center_panel_controller.py
from gui.input.tool_dispatch import ToolDispatch

class CenterPanelController:
    def __init__(self, view, state):
        self.view = view
        self.state = state

        self.dispatch = ToolDispatch(state)

        gw = view.grid_widget
        self.dispatch.attach_widget(gw)   # <-- REQUIRED FIX

        gw.bind("<Button-1>", self.dispatch.on_click)
        gw.bind("<B1-Motion>", self.dispatch.on_drag)
        gw.bind("<ButtonRelease-1>", self.dispatch.on_release)

        # colors etc...
        gw.set_biome_colors({
            "plains": "#b7e590",
            "forest": "#4c9a2a",
            "mountain": "#b0b0b0",
            "swamp": "#5b7e5a",
        })

        ev = state.events
        ev.subscribe("grid_changed", lambda *_: gw.redraw())
        ev.subscribe("party_moved", lambda pos: gw.set_party_positions([pos]))
        ev.subscribe("map_loaded", lambda *_: self._on_map_loaded())

    def _on_map_loaded(self):
        gw = self.view.grid_widget
        gw.grid = self.state.grid
        gw._compute_canvas_size()