# file: simulation/engine.py
from dataclasses import dataclass
import random

from core.grid import HexGrid
from core.party import Party
from core.movement import AXIAL_DIRECTIONS, add


@dataclass
class Scheduler:
    """Tracks world time in 'days'. 6 tokens == 1 daytime."""
    time_days: float = 0.0

    def advance(self, cost: float):
        # 6 tokens = 1 day
        self.time_days += (cost / 6.0)


class SimulationEngine:
    """
    Computes travel cost and applies token + exhaustion penalties.
    Performs NO GUI changes. Party movement is done via MovePartyCommand.

    New responsibilities:
      - Include trail_mod (from trail types) in cost
      - Provide a stealth-check helper for cautious travel
    """

    def __init__(self, grid: HexGrid, party: Party, travel_modes):
        self.grid = grid
        self.party = party
        self.travel_modes = travel_modes
        self.scheduler = Scheduler()

    # ---------------------------------------------------------
    # Trail modifier helper
    # ---------------------------------------------------------
    def _get_trail_mod(self, src, direction_index: int) -> float:
        tile = self.grid.get(src)
        if not tile:
            return 0.0

        trail_id = tile.trails[direction_index]
        if not trail_id or trail_id == "none":
            return 0.0

        if not getattr(self.grid, "trail_lib", None):
            return 0.0

        try:
            tt = self.grid.trail_lib.get(trail_id)
            return tt.cost_mod
        except KeyError:
            return 0.0

    # ---------------------------------------------------------
    # Core movement cost calculation
    # ---------------------------------------------------------
    def calculate_move_cost(self, src, dst, mode_id: str, direction_index: int) -> int:
        mode = self.travel_modes.get(mode_id)

        # biome difficulty
        tile = self.grid.get(dst)
        biome = self.grid.biome_lib.get(tile.biome_id)
        env = getattr(biome, "move_difficulty", 0.0)

        # trail modifier
        trail_mod = self._get_trail_mod(src, direction_index)

        raw_cost = 2 + mode.speed_mod + env + trail_mod
        cost = max(int(round(raw_cost)), 1)

        # ---------------------------------------------
        # DEBUG PRINT (movement cost breakdown)
        # ---------------------------------------------
        print("==== MOVE COST DEBUG ====")
        print(f"Mode: {mode_id}")
        print(f"  Base:             2")
        print(f"  Mode speed_mod:   {mode.speed_mod}")
        print(f"  Biome difficulty: {env}")
        print(f"  Trail modifier:   {trail_mod}")
        print(f"  → Raw cost:       {raw_cost:.2f}")
        print(f"  → Final cost:     {cost}")
        print("-------------------------")

        return cost

    # ---------------------------------------------------------
    # Movement attempt
    # ---------------------------------------------------------
    def move_dir(self, direction_index: int, mode_id: str):
        """
        Computes destination + cost. Does not mutate party/grid.

        Returns:
            (dst_coord, cost) or None if illegal.
        """
        src = self.party.position
        dq, dr = AXIAL_DIRECTIONS[direction_index]
        dst = add(src, (dq, dr))

        if not self.grid.has(dst):
            return None

        cost = self.calculate_move_cost(src, dst, mode_id, direction_index)
        return dst, cost

    # ---------------------------------------------------------
    # Token + exhaustion system
    # ---------------------------------------------------------
    def apply_movement_cost(self, cost: float):
        """
        Apply cost to the entire party and advance world time.
        If a member lacks tokens, overflow becomes exhaustion (handled by Party).
        """
        self.party.apply_movement_cost(cost)
        self.scheduler.advance(cost)

    # ---------------------------------------------------------
    # Stealth check helper (for cautious / stealthy travel)
    # ---------------------------------------------------------
    def perform_stealth_check(self, biome, mode_id: str):
        """
        Simple stealth check: 1d20 vs (biome.stealth_dc + mode.stealth_dc_mod).

        Returns:
            (success: bool, roll: int, dc: int)
        """
        mode = self.travel_modes.get(mode_id)

        base_dc = getattr(biome, "stealth_dc", 12.0)
        dc = base_dc + getattr(mode, "stealth_dc_mod", 0.0)
        dc_int = int(round(dc))

        roll = random.randint(1, 20)

        success = roll >= dc_int

        print("==== STEALTH CHECK DEBUG ====")
        print(f"Mode: {mode_id}")
        print(f"Biome: {biome.id}")
        print(f"  Base DC:          {base_dc}")
        print(f"  Mode dc_mod:      {getattr(mode, 'stealth_dc_mod', 0.0)}")
        print(f"  → Final DC:       {dc_int}")
        print(f"  Roll:             {roll}")
        print(f"  Result:           {'SUCCESS' if success else 'FAILURE'}")
        print("-----------------------------")

        return success, roll, dc_int

    # convenience
    def get_time(self):
        return self.scheduler.time_days

    def reset_time(self):
        self.scheduler.time_days = 0.0