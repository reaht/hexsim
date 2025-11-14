# file: core/serializer.py
import json
from pathlib import Path
from typing import Any, Dict

from .grid import HexGrid
from .party import Party

def save_grid(grid: HexGrid, path: str | Path) -> None:
    data = grid.to_dict()
    path = Path(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_grid(path: str | Path, biome_lib) -> HexGrid:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    from .grid import HexGrid  # local import to avoid circulars at top-level
    return HexGrid.from_dict(data, biome_lib)

def save_party(party: Party, path: str | Path) -> None:
    obj = {
        "position": party.position,
        "leader_index": party.leader_index,
        "members": [m.__dict__ for m in party.members],
    }
    path = Path(path)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

def load_party(path: str | Path) -> Party:
    from .party import PartyMember, Party
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    members = [PartyMember(**m) for m in data["members"]]
    return Party(members, data["leader_index"], tuple(data["position"]))