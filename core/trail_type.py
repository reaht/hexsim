# file: core/trail_type.py
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class TrailType:
    id: str
    name: str
    cost_mod: float
    color: str = "#8b4513"      # default brown
    width: float = 4.0          # line thickness
    description: str = ""


class TrailLibrary:
    def __init__(self):
        self.types: Dict[str, TrailType] = {}

    def load_from_csv(self, path: str | Path):
        path = Path(path)
        if not path.exists():
            # fallback default
            self.add(TrailType("footpath", "Footpath", 1.0))
            self.add(TrailType("road", "Road", 2.0))
            self.add(TrailType("highway", "Highway", 3.0))
            return

        with path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                tt = TrailType(
                    id=row["id"],
                    name=row.get("name", row["id"]),
                    cost_mod=float(row.get("cost_mod", 1.0)),
                    color=row.get("color", "#8b4513"),
                    width=float(row.get("width", 4)),
                    description=row.get("description", ""),
                )
                self.add(tt)

    def add(self, trail: TrailType):
        self.types[trail.id] = trail

    def get(self, tid: str) -> TrailType:
        return self.types[tid]

    def ids(self):
        return list(self.types.keys())