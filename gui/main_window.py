# file: gui/main_window.py
import tkinter as tk
from tkinter import ttk

from gui.app_state import AppState
from gui.grid_widget import HexGridWidget

from gui.ui.toolbar import Toolbar
from gui.ui.biome_panel import BiomePanel
from gui.ui.movement_panel import MovementPanel
from gui.ui.file_menu import FileMenu

# Tools
from gui.tools.select_tool import SelectTool
from gui.tools.inspect_tool import InspectTool
from gui.tools.paint_biome_tool import PaintBiomeTool
from gui.tools.paint_trail_tool import PaintTrailTool
from gui.tools.erase_trail_tool import EraseTrailTool


class MainWindow:
    """
    Builds the full GUI, wires EventBus and tools.
    """

    def __init__(self, root: tk.Tk, state: AppState):
        self.root = root
        self.state = state

        self.current_tool_var = tk.StringVar(value="select")

        self.main = None
        self.left = None
        self.center = None
        self.right = None

        self.grid_widget: HexGridWidget | None = None
        self.toolbar: Toolbar | None = None
        self.biome_panel: BiomePanel | None = None
        self.movement_panel: MovementPanel | None = None
        self.file_menu: FileMenu | None = None

        self._build_layout()
        self._build_left_panel()
        self._build_center_panel()
        self._build_right_panel()
        self._build_menu()
        self._wire_events()

        # Initial party position and draw
        self.state.events.publish("party_moved", self.state.party.position)
        self.state.events.publish("grid_changed")

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    def _build_layout(self):
        self.main = ttk.Frame(self.root)
        self.main.pack(fill="both", expand=True)

        self.left = ttk.Frame(self.main)
        self.left.pack(side="left", fill="y")

        self.center = ttk.Frame(self.main)
        self.center.pack(side="left", fill="both", expand=True)

        self.right = ttk.Frame(self.main)
        self.right.pack(side="left", fill="y")

    # ---------------------------------------------------------
    # Left panel
    # ---------------------------------------------------------

    def _build_left_panel(self):
        biome_ids = self.state.biome_lib.ids()

        self.biome_panel = BiomePanel(self.left, biome_ids)

        tools = {
            "select": SelectTool(),
            "inspect": InspectTool(),
            "paint_biome": PaintBiomeTool(self.biome_panel.biome_var),
            "paint_trail": PaintTrailTool(),
            "erase_trail": EraseTrailTool(),
        }
        self.state.tools = tools

        self.toolbar = Toolbar(self.left, tools, self.current_tool_var)

    # ---------------------------------------------------------
    # Center panel (grid)
    # ---------------------------------------------------------

    def _build_center_panel(self):
        self.grid_widget = HexGridWidget(self.center, self.state.grid, cell_size=32, bg="white")
        self.grid_widget.pack(fill="both", expand=True)

        biome_colors = {
            "plains": "#b7e590",
            "forest": "#4c9a2a",
            "mountain": "#b0b0b0",
            "swamp": "#5b7e5a",
        }
        self.grid_widget.set_biome_colors(biome_colors)

        self.grid_widget.set_on_hex_clicked(self._handle_hex_click)
        self.grid_widget.bind("<B1-Motion>", self._handle_hex_drag)
        self.grid_widget.bind("<ButtonRelease-1>", self._handle_hex_release)

    # ---------------------------------------------------------
    # Right panel (movement)
    # ---------------------------------------------------------

    def _build_right_panel(self):
        self.movement_panel = MovementPanel(self.right, self.state)

    # ---------------------------------------------------------
    # Menu
    # ---------------------------------------------------------

    def _build_menu(self):
        self.file_menu = FileMenu(self.root, self.state)

    # ---------------------------------------------------------
    # EventBus wiring
    # ---------------------------------------------------------

    def _wire_events(self):
        ev = self.state.events

        ev.subscribe("grid_changed", self._on_grid_changed)
        ev.subscribe("party_moved", self._on_party_moved)
        ev.subscribe("map_loaded", self._on_map_loaded)

    def _on_grid_changed(self, *args, **kwargs):
        if self.grid_widget:
            self.grid_widget.redraw()

    def _on_party_moved(self, pos):
        if self.grid_widget:
            self.grid_widget.set_party_positions([pos])

    def _on_map_loaded(self, *args, **kwargs):
        if not self.grid_widget:
            return

        # Re-bind the widget to the new grid
        self.grid_widget.grid = self.state.grid
        self.grid_widget._compute_canvas_size()

    # ---------------------------------------------------------
    # Tool dispatch
    # ---------------------------------------------------------

    def _get_current_tool(self):
        tool_id = self.current_tool_var.get()
        return self.state.tools.get(tool_id)

    def _handle_hex_click(self, coord):
        tool = self._get_current_tool()
        if tool:
            tool.on_click(coord, self.state)

    def _handle_hex_drag(self, event):
        tool = self._get_current_tool()
        if not tool or not self.grid_widget:
            return
        coord = self.grid_widget.pixel_to_hex(event.x, event.y)
        if coord in self.state.grid.tiles:
            tool.on_drag(coord, self.state)

    def _handle_hex_release(self, event):
        tool = self._get_current_tool()
        if tool:
            tool.on_release(self.state)