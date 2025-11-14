# file: simulation/engine.py
from dataclasses import dataclass

from core.grid import HexGrid
from core.party import Party
from core.movement import AXIAL_DIRECTIONS, add, move_party as raw_move
from core.movement import calculate_time_cost


@dataclass
class Scheduler:
    time_tokens: float = 0.0

    def advance(self, dt: float):
        self.time_tokens += dt


class SimulationEngine:
    def __init__(self, grid: HexGrid, party: Party):
        self.grid = grid
        self.party = party
        self.scheduler = Scheduler()

    def move_dir(self, direction_index: int, mode="normal"):
        src = self.party.position
        dq, dr = AXIAL_DIRECTIONS[direction_index]
        dst = add(src, (dq, dr))

        if not self.grid.has(dst):
            print("Movement blocked:", dst)
            return False

        cost = calculate_time_cost(self.party, self.grid, src, dst, mode)

        moved = raw_move(self.party, self.grid, direction_index)
        if not moved:
            return False

        self.scheduler.advance(cost)

        print(
            f"Moved {AXIAL_DIRECTIONS[direction_index]} from {src} to {dst}, "
            f"cost +{cost:.2f}, total {self.scheduler.time_tokens:.2f}"
        )

        return True

    def get_time(self):
        return self.scheduler.time_tokens

    def reset_time(self):
        self.scheduler.time_tokens = 0.0