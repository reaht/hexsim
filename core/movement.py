# file: core/movement.py
from typing import Tuple
from core.grid import HexGrid
from core.party import Party

Coord = Tuple[int, int]  # (q, r) axial coordinates


# ---------------------------------------------------------
# Flat-top axial directions in correct N,NE,SE,S,SW,NW order
# ---------------------------------------------------------
AXIAL_DIRECTIONS = [
    (0, -1),   # 0 = N
    (1, -1),   # 1 = NE
    (1,  0),   # 2 = SE
    (0,  1),   # 3 = S
    (-1, 1),   # 4 = SW
    (-1, 0),   # 5 = NW
]


def add(a: Coord, b: Coord) -> Coord:
    """Add two axial coordinates."""
    return (a[0] + b[0], a[1] + b[1])


# ---------------------------------------------------------
# Basic movement step (no cost)
# ---------------------------------------------------------
def move_party(party: Party, grid: HexGrid, direction_index: int) -> bool:
    """
    Attempts to move the party in one of 6 axial directions.
    Returns True if move succeeded.
    """

    dq, dr = AXIAL_DIRECTIONS[direction_index]
    src = party.position
    dst = add(src, (dq, dr))

    if not grid.has(dst):
        return False

    party.position = dst
    return True


# ---------------------------------------------------------
# Time-token movement cost
# ---------------------------------------------------------

SPEED_MODES = {
    "cautious": 1.5,
    "normal":   1.0,
    "fast":     0.7,
}


def calculate_time_cost(
    party: Party,
    grid: HexGrid,
    src: Coord,
    dst: Coord,
    mode: str = "normal"
) -> float:
    """
    Computes time tokens required to move from axial coord src → dst.
    Uses leader stats and biome difficulty.
    """

    tile_from = grid.get(src)
    tile_to   = grid.get(dst)

    # Missing tile → impossible move
    if tile_from is None or tile_to is None:
        return 9999.0

    biome_from = tile_from.biome_id
    biome_to   = tile_to.biome_id

    # Leader stat factor (example: wisdom affects navigation)
    leader = party.leader
    stat_factor = max(0.3, leader.wisdom / 15.0)

    # Biome difficulties
    b_from = grid.biome_lib.get(biome_from)
    b_to   = grid.biome_lib.get(biome_to)
    base_difficulty = (b_from.base_cost + b_to.base_cost) * 0.5

    # Speed mode modifier
    speed_mult = SPEED_MODES.get(mode, 1.0)

    # Final formula
    cost = base_difficulty * speed_mult / stat_factor
    return cost