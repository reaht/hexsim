# file: gui/windows/left_panel_controller.py
from gui.ui.toolbar import Toolbar
from gui.ui.biome_panel import BiomePanel

from gui.tools.select_tool import SelectTool
from gui.tools.inspect_tool import InspectTool
from gui.tools.paint_biome_tool import PaintBiomeTool
from gui.tools.paint_trail_tool import PaintTrailTool
from gui.tools.erase_trail_tool import EraseTrailTool


class LeftPanelController:
    """
    Handles logic for:
      - Creating tools
      - Wiring toolbar
      - Wiring biome panel
    """

    def __init__(self, view, state):
        self.view = view
        self.state = state

        # Create sub-panels
        biome_ids = state.biome_lib.ids()
        self.view.biome_panel = BiomePanel(self.view.biome_area, biome_ids)

        # Create tool instances
        tools = {
            "select": SelectTool(),
            "inspect": InspectTool(),
            "paint_biome": PaintBiomeTool(self.view.biome_panel.biome_var),
            "paint_trail": PaintTrailTool(),
            "erase_trail": EraseTrailTool(),
        }
        state.tools = tools

        # Create toolbar
        self.view.toolbar = Toolbar(
            self.view.toolbar_area,
            tools,
            state.current_tool_var,
            state
        )