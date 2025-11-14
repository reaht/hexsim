# file: simulation/engine.py
from dataclasses import dataclass

from core.grid import HexGrid
from core.party import Party
from core.movement import AXIAL_DIRECTIONS, add
from core.movement import calculate_time_cost


@dataclass
class Scheduler:
    time_tokens: float = 0.0

    def advance(self, dt: float):
        self.time_tokens += dt


class SimulationEngine:
    """
    The engine now performs **movement resolution** without mutating state.
    Movement becomes undoable in GUI via MovePartyCommand.
    """

    def __init__(self, grid: HexGrid, party: Party):
        self.grid = grid
        self.party = party
        self.scheduler = Scheduler()

    def move_dir(self, direction_index: int, mode="normal"):
        """
        Resolve movement request. Does NOT change party position.

        Returns:
            (dst_coord, cost) if movement is valid
            None if blocked or invalid
        """

        src = self.party.position
        dq, dr = AXIAL_DIRECTIONS[direction_index]
        dst = add(src, (dq, dr))

        if not self.grid.has(dst):
            # Movement blocked by grid boundary or missing tile
            return None

        # Calculate time cost without applying it yet
        cost = calculate_time_cost(self.party, self.grid, src, dst, mode)

        return dst, cost

    def apply_movement_cost(self, cost: float):
        """Tools/commands call this after performing movement."""
        self.scheduler.advance(cost)

    def get_time(self):
        return self.scheduler.time_tokens

    def reset_time(self):
        self.scheduler.time_tokens = 0.0