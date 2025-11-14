# file: core/grid.py
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Any, List

Coord = Tuple[int, int]  # axial (q, r)


@dataclass
class HexTile:
    biome_id: str
    elevation: int = 0
    trails: List[bool] = None      # 6 directions: [N, NE, SE, S, SW, NW]
    data: Dict[str, Any] = None    # free-form extra data

    def __post_init__(self):
        if self.trails is None:
            # 0=N, 1=NE, 2=SE, 3=S, 4=SW, 5=NW
            self.trails = ["none"] * 6
        if self.data is None:
            self.data = {}


class HexGrid:
    """
    A dictionary-based axial coordinate hex map.
    Keys: (q, r)
    Values: HexTile instances
    """

    def __init__(self):
        self.tiles: Dict[Coord, HexTile] = {}
        self.biome_lib = None  # set externally
        self.trail_lib = None

    # ---------------------------------------------------------
    # Tile access
    # ---------------------------------------------------------

    def has(self, coord: Coord) -> bool:
        return coord in self.tiles

    def get(self, coord: Coord) -> Optional[HexTile]:
        return self.tiles.get(coord)

    def set(self, coord: Coord, tile: HexTile):
        self.tiles[coord] = tile

    def set_biome(self, coord: Coord, biome_id: str):
        if coord not in self.tiles:
            self.tiles[coord] = HexTile(biome_id)
        else:
            self.tiles[coord].biome_id = biome_id

    # ---------------------------------------------------------
    # Map generation
    # ---------------------------------------------------------

    def generate_rectangle(self, width: int, height: int, default_biome="plains"):
        """
        Fills a width × height region using axial coordinates:
        q = 0..width-1
        r = 0..height-1
        """
        for q in range(width):
            for r in range(height):
                self.tiles[(q, r)] = HexTile(default_biome)
    
    @staticmethod
    def hex_distance(a, b):
        aq, ar = a
        bq, br = b
        as_ = -aq - ar
        bs = -bq - br
        return max(abs(aq - bq), abs(ar - br), abs(as_ - bs))
    
    def generate_hex_radius(self, radius: int, default_biome="plains"):
        self.tiles.clear()
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                if self.hex_distance((0,0), (q,r)) <= radius:
                    self.tiles[(q,r)] = HexTile(default_biome)
    
    # ---------------------------------------------------------
    # Trail helpers
    # ---------------------------------------------------------

    @staticmethod
    def opposite_dir(direction_index: int) -> int:
        """
        Opposite directions in our 6-dir scheme:
        0<->3 (N<->S), 1<->4 (NE<->SW), 2<->5 (SE<->NW)
        """
        return (direction_index + 3) % 6

    def set_trail(self, coord, direction_index: int, value: str):
        tile = self.tiles.get(coord)
        if tile is None:
            return

        # Set on this tile
        tile.trails[direction_index] = value

        # Mirror to neighbor
        from core.movement import AXIAL_DIRECTIONS, add

        dq, dr = AXIAL_DIRECTIONS[direction_index]
        neighbor_coord = add(coord, (dq, dr))
        neighbor = self.tiles.get(neighbor_coord)
        if neighbor is not None:
            opp = self.opposite_dir(direction_index)
            neighbor.trails[opp] = value

    # ---------------------------------------------------------
    # Save / Load
    # ---------------------------------------------------------

    def to_dict(self):
        return {
            "tiles": [
                {
                    "q": q,
                    "r": r,
                    "biome": t.biome_id,
                    "elevation": t.elevation,
                    "trails": t.trails,
                    "data": t.data,
                }
                for (q, r), t in self.tiles.items()
            ]
        }

    @classmethod
    def from_dict(cls, data):
        g = cls()
        for item in data["tiles"]:
            q, r = item["q"], item["r"]
            biome = item.get("biome", "plains")
            elevation = item.get("elevation", 0)
            trails = item.get("trails", ["none"] * 6)
            extra = item.get("data", {})
            g.tiles[(q, r)] = HexTile(
                biome_id=biome,
                elevation=elevation,
                trails=trails,
                data=extra,
            )
        return g

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def coords(self):
        return self.tiles.keys()