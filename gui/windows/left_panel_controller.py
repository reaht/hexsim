# file: gui/windows/left_panel_controller.py
from gui.ui.toolbar import Toolbar
from gui.ui.biome_panel import BiomePanel

from gui.tools.select_tool import SelectTool
from gui.tools.inspect_tool import InspectTool
from gui.tools.paint_biome_tool import PaintBiomeTool
from gui.tools.paint_trail_tool import PaintTrailTool
from gui.tools.erase_trail_tool import EraseTrailTool
from gui.ui.trail_panel import TrailPanel

class LeftPanelController:
    def __init__(self, view, state):
        self.view = view
        self.state = state

        # --- Biomes ---
        biome_ids = state.biome_lib.ids()
        self.view.biome_panel = BiomePanel(self.view.biome_area, biome_ids)

        # --- Trails ---
        trail_ids = state.grid.trail_lib.ids()
        self.view.trail_panel = TrailPanel(self.view.trail_area, trail_ids)

        # Connect AppState -> selected trail
        state.current_trail_var = self.view.trail_panel.trail_var   # ✅ CRITICAL

        # Tools (unchanged except paint_trail)
        tools = {
            "select": SelectTool(),
            "inspect": InspectTool(),
            "paint_biome": PaintBiomeTool(self.view.biome_panel.biome_var),
            "paint_trail": PaintTrailTool(),       # now reads state.current_trail_var
            "erase_trail": EraseTrailTool(),
        }
        state.tools = tools

        # Toolbar
        self.view.toolbar = Toolbar(
            self.view.toolbar_area,
            tools,
            state.current_tool_var,
            state,
        )