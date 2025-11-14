# file: core/hex_math.py
import math
from typing import Tuple

Coord = Tuple[int, int]


class HexMath:
    """
    Flat-top axial hex coordinate <-> pixel conversion.
    Shared by any widget/renderer that needs hex math.
    """

    def __init__(self, size: float, offset_x: float = 0.0, offset_y: float = 0.0):
        self.s = size
        self.offset_x = offset_x
        self.offset_y = offset_y

    # ---------------------------------------------------------
    # Offsets (for centering, padding, etc.)
    # ---------------------------------------------------------

    def set_offset(self, offset_x: float, offset_y: float) -> None:
        self.offset_x = offset_x
        self.offset_y = offset_y

    # ---------------------------------------------------------
    # Axial -> pixel
    # ---------------------------------------------------------

    def axial_to_pixel_raw(self, q: int, r: int) -> Tuple[float, float]:
        """
        Convert axial (q, r) to pixel coordinates with origin at (0,0),
        without applying the widget's offset.
        """
        s = self.s
        x = s * 1.5 * q
        y = s * math.sqrt(3) * (r + q / 2)
        return (x, y)

    def axial_to_pixel(self, q: int, r: int) -> Tuple[float, float]:
        """
        Convert axial (q, r) to pixel coordinates including offsets.
        """
        x, y = self.axial_to_pixel_raw(q, r)
        return (x + self.offset_x, y + self.offset_y)

    # ---------------------------------------------------------
    # Pixel -> axial
    # ---------------------------------------------------------

    def pixel_to_axial(self, x: float, y: float) -> Coord:
        """
        Convert pixel coordinates (x, y) back to *rounded* axial hex coords.
        """
        x -= self.offset_x
        y -= self.offset_y
        s = self.s

        q = (2.0 / 3.0 * x) / s
        r = (-1.0 / 3.0 * x + (math.sqrt(3) / 3.0) * y) / s

        return self._cube_round(self._axial_to_cube(q, r))

    # ---------------------------------------------------------
    # Internal cube helpers
    # ---------------------------------------------------------

    def _axial_to_cube(self, q: float, r: float):
        # cube coords: x=q, z=r, y=-x-z
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

        # return axial (q, r) from cube (x, y, z)
        return (int(rx), int(rz))