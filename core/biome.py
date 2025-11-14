# file: core/biome.py
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class Biome:
    id: str
    name: str
    base_cost: float
    danger: float
    move_difficulty: float = 0.0
    color: str = "#cccccc"      # NEW
    description: str = ""


class BiomeLibrary:
    def __init__(self):
        self.biomes: Dict[str, Biome] = {}

    def load_from_csv(self, path: str | Path):
        path = Path(path)
        if not path.exists():
            # fallback defaults
            self.add(Biome("plains", "Plains", 1.0, 0.2, 0, "#d9e86c"))
            self.add(Biome("forest", "Forest", 2.0, 0.8, 1, "#3a6b32"))
            self.add(Biome("mountain", "Mountain", 3.0, 1.5, 2, "#8d8c8c"))
            self.add(Biome("swamp", "Swamp", 3.0, 1.0, 1, "#4f5b2a"))
            return

        with path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                biome = Biome(
                    id=row["id"],
                    name=row.get("name", row["id"]),
                    base_cost=float(row.get("base_cost", 1)),
                    danger=float(row.get("danger", 0)),
                    move_difficulty=float(row.get("move_difficulty", 0)),
                    color=row.get("color", "#cccccc"),        # NEW
                    description=row.get("description", "")
                )
                self.add(biome)

    def add(self, biome: Biome):
        self.biomes[biome.id] = biome

    def get(self, biome_id: str) -> Biome:
        return self.biomes[biome_id]

    def ids(self):
        return list(self.biomes.keys())