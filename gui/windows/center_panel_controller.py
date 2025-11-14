# file: gui/windows/center_panel_controller.py
from gui.input.tool_dispatch import ToolDispatch


class CenterPanelController:
    """
    Wires together:
      - Pixel → hex interactions
      - Tool dispatch
      - Redraw events
      - Party position updates
    """

    def __init__(self, view, state):
        self.view = view
        self.state = state

        gw = view.grid_widget

        # ---------------------------------------------------------
        # Tool dispatch wiring
        # ---------------------------------------------------------
        self.dispatch = ToolDispatch(state)
        self.dispatch.attach_widget(gw)

        gw.bind("<Button-1>", self.dispatch.on_click)
        gw.bind("<B1-Motion>", self.dispatch.on_drag)
        gw.bind("<ButtonRelease-1>", self.dispatch.on_release)

        # ---------------------------------------------------------
        # Biome colors now come from the BiomeLibrary CSV
        # So we REMOVE the old hardcoded set_biome_colors() call.
        #
        # TileLayer will internally ask grid.biome_lib for tile color.
        # ---------------------------------------------------------

        # If desired, keep a compatibility call (does nothing)
        if hasattr(gw, "set_biome_colors"):
            gw.set_biome_colors({})  # Provide empty map for compatibility only

        # ---------------------------------------------------------
        # Event subscriptions
        # ---------------------------------------------------------
        ev = state.events
        ev.subscribe("grid_changed", lambda *_: gw.redraw())
        ev.subscribe("party_moved", lambda pos: gw.set_party_positions([pos]))
        ev.subscribe("map_loaded", lambda *_: self._on_map_loaded())

    # ---------------------------------------------------------
    # Reload handler
    # ---------------------------------------------------------
    def _on_map_loaded(self):
        gw = self.view.grid_widget
        gw.grid = self.state.grid
        gw._compute_canvas_size()