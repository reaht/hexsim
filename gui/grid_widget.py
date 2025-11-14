# file: gui/grid_widget.py
import tkinter as tk
from typing import Callable, Tuple, Optional, List

from core.grid import HexGrid
from core.hex_math import HexMath

from gui.renderers.layered_renderer import LayeredRenderer
from gui.renderers.layers.tile_layer import TileLayer
from gui.renderers.layers.trail_layer import TrailLayer
from gui.renderers.layers.party_layer import PartyLayer
from gui.renderers.layers.gridline_layer import GridlineLayer
from gui.renderers.layers.selection_layer import SelectionLayer

Coord = Tuple[int, int]


class HexGridWidget(tk.Canvas):
    """
    Canvas-based hex grid widget with layered rendering.
    After resizing the canvas, we WAIT (after 100ms) before centering
    because Tk must finish layout before winfo_width/height are accurate.
    """

    def __init__(self, master, grid: HexGrid, cell_size=32, **kwargs):
        super().__init__(master, **kwargs)

        self.grid = grid
        self.party_positions: List[Coord] = []
        self.on_hex_clicked: Optional[Callable[[Coord], None]] = None

        # Offsets set after layout
        self.hex_math = HexMath(size=cell_size, offset_x=0, offset_y=0)

        # Layers
        self.tile_layer = TileLayer(self, self.hex_math)
        self.grid_layer = GridlineLayer(self, self.hex_math)
        self.trail_layer = TrailLayer(self, self.hex_math)
        self.party_layer = PartyLayer(self, self.hex_math)
        self.selection_layer = SelectionLayer(self, self.hex_math)

        self.renderer = LayeredRenderer(
            self, layers=[
                self.tile_layer,
                self.grid_layer,
                self.trail_layer,
                self.party_layer,
                self.selection_layer,
            ]
        )

        # Mouse
        self.bind("<Button-1>", self._click)
        self.bind("<B1-Motion>", self._drag)
        self.bind("<Motion>", self._hover)
        self.bind("<Leave>", self._leave_hover)

        self._last_drag: Optional[Coord] = None

        # Start delayed layout
        self.after(500, self._post_init_layout)

    # ---------------------------------------------------------
    # Full post-init sequence: resize canvas → wait → center map
    # ---------------------------------------------------------
    def _post_init_layout(self):
        """Run initial layout after Tk has sized widgets once."""
        self._compute_canvas_size()

        # Wait for geometry propagation before centering
        self.after(500, self._delayed_center_and_redraw)

    def _delayed_center_and_redraw(self):
        """Second-stage layout: now canvas dimensions are correct."""
        self._center_map()
        self.redraw()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def set_biome_colors(self, mapping):
        self.redraw()  # kept for compatibility only

    def set_party_positions(self, positions: List[Coord]):
        self.party_positions = positions
        self.redraw()

    def set_on_hex_clicked(self, callback: Callable[[Coord], None]):
        self.on_hex_clicked = callback

    def pixel_to_hex(self, x: float, y: float) -> Coord:
        return self.hex_math.pixel_to_axial(x, y)

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------
    def _click(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        self._last_drag = coord

        if coord in self.grid.tiles:
            self.selection_layer.set_selected(coord)
            self.redraw()

        if self.on_hex_clicked and coord in self.grid.tiles:
            self.on_hex_clicked(coord)

    def _drag(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        if coord != self._last_drag and coord in self.grid.tiles:
            self._last_drag = coord
            if self.on_hex_clicked:
                self.on_hex_clicked(coord)

    def _hover(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        self.selection_layer.set_hovered(coord if coord in self.grid.tiles else None)
        self.redraw()

    def _leave_hover(self, event):
        self.selection_layer.set_hovered(None)
        self.redraw()

    # ---------------------------------------------------------
    # Compute bounding box
    # ---------------------------------------------------------
    def _compute_canvas_size(self):
        """Compute map bounding box in pixels, set canvas size."""
        if not self.grid.tiles:
            return

        qs = [q for (q, _) in self.grid.tiles]
        rs = [r for (_, r) in self.grid.tiles]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        # Compute raw pixel box from HEX CENTERS (faster & adequate)
        px_min_x, px_min_y = self.hex_math.axial_to_pixel_raw(min_q, min_r)
        px_max_x, px_max_y = self.hex_math.axial_to_pixel_raw(max_q, max_r)

        map_w = abs(px_max_x - px_min_x)
        map_h = abs(px_max_y - px_min_y)

        pad = self.hex_math.s * 4

        width = int(map_w + pad)
        height = int(map_h + pad)

        # Apply canvas size
        self.config(width=width, height=height)

        # Save for centering
        self._map_width = map_w
        self._map_height = map_h

        # Debug output
        print("=== GRID SIZE DEBUG ===")
        print(f"min_q,max_q = {min_q},{max_q}")
        print(f"min_r,max_r = {min_r},{max_r}")
        print(f"pixel bounds = ({px_min_x},{px_min_y}) to ({px_max_x},{px_max_y})")
        print(f"map_w,map_h = {map_w},{map_h}")
        print(f"canvas set to {width}×{height}")

    # ---------------------------------------------------------
    # Center the map AFTER canvas size is correct
    # ---------------------------------------------------------
    def _center_map(self):
        canvas_w = self.winfo_width()
        canvas_h = self.winfo_height()

        if canvas_w <= 1 or canvas_h <= 1:
            print("Center skipped: canvas not ready")
            return

        # Centering
        self.hex_math.offset_x = canvas_w // 2# - self._map_width // 2
        self.hex_math.offset_y = canvas_h // 2# - self._map_height // 2

        print("=== CENTER MAP DEBUG ===")
        print(f"canvas: {canvas_w}×{canvas_h}")
        print(f"offset_x={self.hex_math.offset_x}")
        print(f"offset_y={self.hex_math.offset_y}")

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------
    def redraw(self):
        self.renderer.draw(self.grid, self.party_positions)