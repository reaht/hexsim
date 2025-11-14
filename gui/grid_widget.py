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
    Biome colors now come directly from BiomeLibrary (CSV).
    """

    def __init__(self, master, grid: HexGrid, cell_size=32, **kwargs):
        super().__init__(master, **kwargs)

        self.grid = grid
        self.party_positions: List[Coord] = []

        self.on_hex_clicked: Optional[Callable[[Coord], None]] = None

        # ---------------------------------------------------------
        # Coordinate math
        # ---------------------------------------------------------
        self.hex_math = HexMath(
            size=cell_size,
            offset_x=cell_size * 2,
            offset_y=cell_size * 2,
        )

        # ---------------------------------------------------------
        # Layers
        # ---------------------------------------------------------
        # biome_colors={} is now unused — TileLayer pulls from BiomeLibrary
        self.tile_layer = TileLayer(self, self.hex_math)
        self.grid_layer = GridlineLayer(self, self.hex_math)
        self.trail_layer = TrailLayer(self, self.hex_math)
        self.party_layer = PartyLayer(self, self.hex_math)
        self.selection_layer = SelectionLayer(self, self.hex_math)

        self.renderer = LayeredRenderer(
            self,
            layers=[
                self.tile_layer,
                self.grid_layer,
                self.trail_layer,
                self.party_layer,
                self.selection_layer,
            ],
        )

        # ---------------------------------------------------------
        # Mouse Input
        # ---------------------------------------------------------
        self.bind("<Button-1>", self._click)
        self.bind("<B1-Motion>", self._drag)
        self.bind("<Motion>", self._hover)
        self.bind("<Leave>", self._leave_hover)

        self._last_drag: Optional[Coord] = None

        self._compute_canvas_size()
        self.redraw()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_biome_colors(self, mapping):
        """
        Deprecated — kept only for compatibility with old controllers.
        Biome colors are now read directly from the CSV (BiomeLibrary).
        """
        # Do nothing, but allow calls
        self.redraw()

    def set_party_positions(self, positions: List[Coord]):
        self.party_positions = positions
        self.redraw()

    def set_on_hex_clicked(self, callback: Callable[[Coord], None]):
        self.on_hex_clicked = callback

    def pixel_to_hex(self, x: float, y: float) -> Coord:
        return self.hex_math.pixel_to_axial(x, y)

    # ---------------------------------------------------------
    # Event Handling
    # ---------------------------------------------------------

    def _click(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        self._last_drag = coord

        if coord in self.grid.tiles:
            self.selection_layer.set_selected(coord)
            self.redraw()

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    def _drag(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        if coord == self._last_drag:
            return
        self._last_drag = coord

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    def _hover(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        if coord in self.grid.tiles:
            self.selection_layer.set_hovered(coord)
        else:
            self.selection_layer.set_hovered(None)
        self.redraw()

    def _leave_hover(self, event):
        self.selection_layer.set_hovered(None)
        self.redraw()

    # ---------------------------------------------------------
    # Sizing
    # ---------------------------------------------------------

    def _compute_canvas_size(self):
        if not self.grid.tiles:
            return

        qs = [q for (q, _) in self.grid.tiles]
        rs = [r for (_, r) in self.grid.tiles]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        corners = []
        for q in (min_q, max_q):
            for r in (min_r, max_r):
                corners.append(self.hex_math.axial_to_pixel_raw(q, r))

        xs = [x for x, _ in corners]
        ys = [y for _, y in corners]

        width = int(max(xs) - min(xs) + self.hex_math.s * 4)
        height = int(max(ys) - min(ys) + self.hex_math.s * 4)

        self.config(width=width, height=height)

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def redraw(self):
        self.renderer.draw(self.grid, self.party_positions)