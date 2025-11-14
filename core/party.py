# file: core/party.py
import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple
import math

Coord = Tuple[int, int]


def compute_max_tokens(speed: int, con: int) -> int:
    """
    max_tokens = floor(min(speed*2/5, con*3/5))
    """
    return int(math.floor(min(speed * 2 / 5, con * 3 / 5)))


@dataclass
class PartyMember:
    name: str
    speed: int
    con: int

    max_tokens: int = field(init=False)
    tokens: float = field(init=False)
    exhaustion: float = 0.0

    def __post_init__(self):
        self.max_tokens = compute_max_tokens(self.speed, self.con)
        self.tokens = float(self.max_tokens)

    def apply_cost(self, cost: float):
        """
        Pay cost using tokens; overflow becomes exhaustion.
        """
        if self.tokens >= cost:
            self.tokens -= cost
        else:
            deficit = cost - self.tokens
            self.tokens = 0
            self.exhaustion += deficit


class Party:
    def __init__(self, members: List[PartyMember], leader_index: int, position: Coord):
        self.members = members
        self.leader_index = leader_index
        self.position = position

    @property
    def leader(self) -> PartyMember:
        return self.members[self.leader_index]

    def apply_movement_cost(self, cost: float):
        """
        Apply travel cost to all party members.
        Overflow adds exhaustion.
        """
        for m in self.members:
            m.apply_cost(cost)


def load_party_from_csv(path: str | Path, leader_index=0, start_pos=(0, 0)) -> Party:
    path = Path(path)
    members: List[PartyMember] = []

    if not path.exists():
        members.append(PartyMember("Arden", 30, 10))
        members.append(PartyMember("Lira", 25, 12))
        return Party(members, leader_index, start_pos)

    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            m = PartyMember(
                name=row["name"],
                speed=int(row.get("speed", 30)),
                con=int(row.get("con", 10)),
            )
            members.append(m)

    return Party(members, leader_index, start_pos)