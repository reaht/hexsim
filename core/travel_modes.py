# file: core/travel_modes.py
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class TravelMode:
    id: str
    name: str
    speed_mod: float       # modifies movement cost (negative = faster)
    description: str = ""


class TravelModeLibrary:
    """
    Loads and stores all available travel modes.
    Travel modes come from config/travel_modes.csv.
    """

    def __init__(self):
        self.modes: Dict[str, TravelMode] = {}

    def load_from_csv(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            # fallback defaults
            self.add(TravelMode("reckless", "Reckless", -1, "Fast movement with risk"))
            self.add(TravelMode("normal", "Normal", 0, "Standard travel pace"))
            self.add(TravelMode("cautious", "Cautious", 1, "Slower, stealthier movement"))
            self.add(TravelMode("exploring", "Exploring", 2, "Thorough scouting"))
            self.add(TravelMode("trailblazing", "Trailblazing", 1, "Creates trails while moving"))
            return

        with path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                mode = TravelMode(
                    id=row["id"],
                    name=row.get("name", row["id"]),
                    speed_mod=float(row.get("speed_mod", 0)),
                    description=row.get("description", ""),
                )
                self.add(mode)

    def add(self, mode: TravelMode):
        self.modes[mode.id] = mode

    def get(self, mid: str) -> TravelMode:
        return self.modes[mid]

    def ids(self):
        return list(self.modes.keys())