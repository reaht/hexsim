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
    color: str = "#cccccc"
    stealth_dc: float = 12.0          # NEW: default stealth DC
    description: str = ""


class BiomeLibrary:
    """
    Loads biome definitions from config/biomes.csv.

    Expected CSV columns (extra columns ignored):
      id,name,base_cost,danger,move_difficulty,color[,stealth_dc,description]
    """

    def __init__(self):
        self.biomes: Dict[str, Biome] = {}

    def load_from_csv(self, path: str | Path):
        path = Path(path)
        if not path.exists():
            # fallback defaults with colors and rough stealth DCs
            self.add(Biome("plains", "Plains", 1.0, 0.2, 0, "#d9e86c", 12))
            self.add(Biome("forest", "Forest", 2.0, 0.8, 1, "#3a6b32", 14))
            self.add(Biome("mountain", "Mountain", 3.0, 1.5, 2, "#8d8c8c", 15))
            self.add(Biome("swamp", "Swamp", 3.0, 1.0, 1, "#4f5b2a", 13))
            return

        with path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                # your current CSV has no stealth_dc column yet;
                # default to 12.0 unless explicitly provided
                try:
                    stealth_dc = float(row.get("stealth_dc", 12))
                except ValueError:
                    stealth_dc = 12.0

                biome = Biome(
                    id=row["id"],
                    name=row.get("name", row["id"]),
                    base_cost=float(row.get("base_cost", 1)),
                    danger=float(row.get("danger", 0)),
                    move_difficulty=float(row.get("move_difficulty", 0)),
                    color=row.get("color", "#cccccc"),
                    stealth_dc=stealth_dc,
                    description=row.get("description", ""),
                )
                self.add(biome)

    def add(self, biome: Biome):
        self.biomes[biome.id] = biome

    def get(self, biome_id: str) -> Biome:
        return self.biomes[biome_id]

    def ids(self):
        return list(self.biomes.keys())