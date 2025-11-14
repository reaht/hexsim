# file: core/party.py
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

Coord = Tuple[int, int]


@dataclass
class PartyMember:
    name: str
    strength: int
    dex: int
    wisdom: int
    speed: int


class Party:
    def __init__(self, members: List[PartyMember], leader_index: int, position: Coord):
        self.members = members
        self.leader_index = leader_index
        self.position = position

    @property
    def leader(self) -> PartyMember:
        return self.members[self.leader_index]


def load_party_from_csv(path: str | Path, leader_index=0, start_pos=(0, 0)) -> Party:
    path = Path(path)
    members: List[PartyMember] = []

    if not path.exists():
        members.append(PartyMember("Arden", 14, 13, 10, 30))
        members.append(PartyMember("Lira", 10, 16, 12, 25))
        return Party(members, leader_index, start_pos)

    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            members.append(
                PartyMember(
                    name=row["name"],
                    strength=int(row.get("strength", 10)),
                    dex=int(row.get("dex", 10)),
                    wisdom=int(row.get("wisdom", 10)),
                    speed=int(row.get("speed", 30)),
                )
            )

    return Party(members, leader_index, start_pos)