# file: gui/renderers/hex_renderer.py
import math
import tkinter as tk
from typing import Dict, List, Tuple

from core.movement import AXIAL_DIRECTIONS
from core.grid import HexGrid, HexTile
from core.hex_math import HexMath

Coord = Tuple[int, int]


class HexGridRenderer:
    """
    Responsible only for drawing the hex grid, trails, and party markers
    onto a Tkinter Canvas, using HexMath for coordinate transforms.
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        hex_math: HexMath,
        biome_colors: Dict[str, str] | None = None,
    ):
        self.canvas = canvas
        self.hex_math = hex_math
        self.biome_colors: Dict[str, str] = biome_colors or {}

    def set_biome_colors(self, mapping: Dict[str, str]) -> None:
        self.biome_colors = mapping

    def draw(self, grid: HexGrid, party_positions: List[Coord]) -> None:
        """
        Clear the canvas and redraw the entire scene.
        """
        c = self.canvas
        c.delete("all")
        s = self.hex_math.s

        # Tiles + trails
        for (q, r), tile in grid.tiles.items():
            cx, cy = self.hex_math.axial_to_pixel(q, r)
            color = self.biome_colors.get(tile.biome_id, "#cccccc")
            self._draw_hex(cx, cy, s, color, "black")
            self._draw_trails(cx, cy, s, tile.trails)

        # Party markers
        for (q, r) in party_positions:
            cx, cy = self.hex_math.axial_to_pixel(q, r)
            radius = s * 0.35
            c.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                fill="red",
                outline="black",
                width=2,
            )

    # ---------------------------------------------------------
    # Internal drawing helpers
    # ---------------------------------------------------------

    def _draw_hex(self, cx: float, cy: float, s: float, fill: str, outline: str) -> None:
        pts = []
        for i in range(6):
            angle = math.radians(60 * i)
            pts.append(cx + s * math.cos(angle))
            pts.append(cy + s * math.sin(angle))
        self.canvas.create_polygon(pts, fill=fill, outline=outline, width=1)

    def _draw_trails(self, cx: float, cy: float, s: float, trails: List[bool]) -> None:
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

            # Vector from this hex center to neighbor center, relative to (0,0).
            dx, dy = self.hex_math.axial_to_pixel_raw(dq, dr)

            # Shorten so the trail stays inside the hex
            scale = 0.4
            x2 = cx + dx * scale
            y2 = cy + dy * scale

            self.canvas.create_line(
                cx,
                cy,
                x2,
                y2,
                width=4,
                fill="brown",
                capstyle="round",
            )