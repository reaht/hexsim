# file: gui/grid_widget.py
import tkinter as tk
from typing import Callable, Dict, Tuple, Optional, List

from core.grid import HexGrid
from core.hex_math import HexMath
from gui.renderers.hex_renderer import HexGridRenderer

Coord = Tuple[int, int]


class HexGridWidget(tk.Canvas):
    """
    Tkinter Canvas wrapper that:
      - knows about a HexGrid and party positions
      - converts mouse events to hex coords
      - delegates drawing to HexGridRenderer
      - delegates axial <-> pixel math to HexMath

    Note: click and drag both call on_hex_clicked(coord), so higher-level
    code (gui_main + tools) can implement brushes (biome, roads, etc.).
    """

    def __init__(self, master, grid: HexGrid, cell_size=32, **kwargs):
        super().__init__(master, **kwargs)

        self.grid = grid
        self.party_positions: List[Coord] = []
        self.on_hex_clicked: Optional[Callable[[Coord], None]] = None

        # Hex math & offsets
        self.hex_math = HexMath(size=cell_size, offset_x=cell_size * 2, offset_y=cell_size * 2)

        # Renderer handles all visual drawing
        self.renderer = HexGridRenderer(canvas=self, hex_math=self.hex_math)

        # Mouse interaction
        self.bind("<Button-1>", self._click)
        self.bind("<B1-Motion>", self._drag)
        self._last_drag_coord: Optional[Coord] = None

        # Canvas sizing based on grid content
        self._compute_canvas_size()
        self.redraw()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_biome_colors(self, mapping: Dict[str, str]) -> None:
        self.renderer.set_biome_colors(mapping)
        self.redraw()

    def set_party_positions(self, positions: List[Coord]) -> None:
        self.party_positions = positions
        self.redraw()

    def set_on_hex_clicked(self, callback: Callable[[Coord], None]) -> None:
        self.on_hex_clicked = callback

    # Keep this for external code (tools, gui_main) that uses pixel_to_hex:
    def pixel_to_hex(self, x: float, y: float) -> Coord:
        return self.hex_math.pixel_to_axial(x, y)

    # ---------------------------------------------------------
    # Canvas sizing
    # ---------------------------------------------------------

    def _compute_canvas_size(self) -> None:
        if not self.grid.tiles:
            return

        qs = [q for (q, r) in self.grid.tiles]
        rs = [r for (q, r) in self.grid.tiles]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        corners = []
        for q in (min_q, max_q):
            for r in (min_r, max_r):
                # raw coords: no offset
                corners.append(self.hex_math.axial_to_pixel_raw(q, r))

        xs = [x for x, y in corners]
        ys = [y for x, y in corners]

        width = int(max(xs) - min(xs) + self.hex_math.s * 4)
        height = int(max(ys) - min(ys) + self.hex_math.s * 4)

        self.config(width=width, height=height)

    # ---------------------------------------------------------
    # Mouse interaction
    # ---------------------------------------------------------

    def _click(self, event) -> None:
        coord = self.pixel_to_hex(event.x, event.y)
        self._last_drag_coord = coord

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    def _drag(self, event) -> None:
        coord = self.pixel_to_hex(event.x, event.y)
        if coord == self._last_drag_coord:
            return
        self._last_drag_coord = coord

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------

    def redraw(self) -> None:
        """
        Redraw the entire grid and party markers.
        """
        self.renderer.draw(self.grid, self.party_positions)