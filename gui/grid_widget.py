# file: gui/grid_widget.py
import math
import tkinter as tk
from typing import Callable, Dict, Tuple, Optional, List

from core.grid import HexGrid, HexTile
from core.movement import AXIAL_DIRECTIONS

Coord = Tuple[int, int]


class HexGridWidget(tk.Canvas):
    """
    Draws a dictionary-based axial hex map (flat-top, north-aligned),
    and renders trails stored in each HexTile.

    Note: click and drag both call on_hex_clicked(coord), so higher-level
    code (gui_main) can implement brushes (biome, roads, etc.).
    """

    def __init__(self, master, grid: HexGrid, cell_size=32, **kwargs):
        super().__init__(master, **kwargs)

        self.grid = grid
        self.s = cell_size

        self.biome_colors: Dict[str, str] = {}
        self.party_positions: List[Coord] = []
        self.on_hex_clicked: Optional[Callable[[Coord], None]] = None

        # Padding around map
        self.offset_x = cell_size * 2
        self.offset_y = cell_size * 2

        self.bind("<Button-1>", self._click)

        # drag-paint support
        self.bind("<B1-Motion>", self._drag)
        self._last_drag_coord: Optional[Coord] = None

        self._compute_canvas_size()
        self.redraw()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_biome_colors(self, mapping: Dict[str, str]):
        self.biome_colors = mapping
        self.redraw()

    def set_party_positions(self, positions: List[Coord]):
        self.party_positions = positions
        self.redraw()

    def set_on_hex_clicked(self, callback: Callable[[Coord], None]):
        self.on_hex_clicked = callback

    # ---------------------------------------------------------
    # Canvas sizing
    # ---------------------------------------------------------

    def _compute_canvas_size(self):
        if not self.grid.tiles:
            return

        qs = [q for (q, r) in self.grid.tiles]
        rs = [r for (q, r) in self.grid.tiles]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        corners = []
        for q in (min_q, max_q):
            for r in (min_r, max_r):
                corners.append(self.hex_to_pixel_raw(q, r))

        xs = [x for x, y in corners]
        ys = [y for x, y in corners]

        width = int(max(xs) - min(xs) + self.s * 4)
        height = int(max(ys) - min(ys) + self.s * 4)

        self.config(width=width, height=height)

    # ---------------------------------------------------------
    # Axial → pixel (flat-top)
    # ---------------------------------------------------------

    def hex_to_pixel_raw(self, q: int, r: int) -> Tuple[float, float]:
        s = self.s
        x = s * 1.5 * q
        y = s * math.sqrt(3) * (r + q / 2)
        return (x, y)

    def hex_to_pixel(self, q: int, r: int) -> Tuple[float, float]:
        x, y = self.hex_to_pixel_raw(q, r)
        return (x + self.offset_x, y + self.offset_y)

    # ---------------------------------------------------------
    # Pixel → axial (flat-top inverse)
    # ---------------------------------------------------------

    def pixel_to_hex(self, x: float, y: float) -> Coord:
        x -= self.offset_x
        y -= self.offset_y
        s = self.s

        q = (2.0 / 3.0 * x) / s
        r = (-1.0 / 3.0 * x + (math.sqrt(3) / 3.0) * y) / s

        return self._cube_round(self._axial_to_cube((q, r)))

    def _axial_to_cube(self, coord):
        q, r = coord
        return (q, -q - r, r)

    def _cube_round(self, cube):
        x, y, z = cube
        rx, ry, rz = round(x), round(y), round(z)

        dx, dy, dz = abs(rx - x), abs(ry - y), abs(rz - z)

        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return (int(rx), int(rz))

    # ---------------------------------------------------------
    # Mouse interaction
    # ---------------------------------------------------------

    def _click(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        self._last_drag_coord = coord

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    def _drag(self, event):
        coord = self.pixel_to_hex(event.x, event.y)
        if coord == self._last_drag_coord:
            return
        self._last_drag_coord = coord

        if coord in self.grid.tiles and self.on_hex_clicked:
            self.on_hex_clicked(coord)

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------

    def redraw(self):
        self.delete("all")
        s = self.s

        # Draw tiles + trails
        for (q, r), tile in self.grid.tiles.items():
            cx, cy = self.hex_to_pixel(q, r)
            color = self.biome_colors.get(tile.biome_id, "#cccccc")
            self._draw_hex(cx, cy, s, color, "black")
            self._draw_trails(cx, cy, s, tile.trails)

        # Draw party markers
        for (q, r) in self.party_positions:
            cx, cy = self.hex_to_pixel(q, r)
            radius = s * 0.35
            self.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill="red", outline="black", width=2
            )

    def _draw_hex(self, cx: float, cy: float, s: float, fill: str, outline: str):
        pts = []
        for i in range(6):
            angle = math.radians(60 * i)
            pts.append(cx + s * math.cos(angle))
            pts.append(cy + s * math.sin(angle))
        self.create_polygon(pts, fill=fill, outline=outline, width=1)

    def _draw_trails(self, cx: float, cy: float, s: float, trails: List[bool]):
        """
        Draw trail segments from center toward the actual neighbor centers.
        Direction order matches AXIAL_DIRECTIONS:
        0=N, 1=NE, 2=SE, 3=S, 4=SW, 5=NW
        """
        if not trails:
            return

        for dir_index, has_trail in enumerate(trails):
            if not has_trail:
                continue

            dq, dr = AXIAL_DIRECTIONS[dir_index]
            dx, dy = self.hex_to_pixel_raw(dq, dr)

            scale = 0.4
            x2 = cx + dx * scale
            y2 = cy + dy * scale

            self.create_line(
                cx, cy, x2, y2,
                width=4,
                fill="brown",
                capstyle="round"
            )