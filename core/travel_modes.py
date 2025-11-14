# file: core/travel_modes.py
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class TravelMode:
    id: str
    name: str
    speed_mod: float       # modifies movement cost (negative = faster)
    description: str = ""
    # NEW: stealth modifier and optional trail type
    stealth_dc_mod: float = 0.0
    trail_type: Optional[str] = None   # e.g. "footpath" when trailblazing


class TravelModeLibrary:
    """
    Loads and stores all available travel modes.
    Travel modes come from config/travel_modes.csv.

    Expected CSV columns (extra columns are optional):
      id,name,speed_mod,description[,stealth_dc_mod,trail_type]
    """

    def __init__(self):
        self.modes: Dict[str, TravelMode] = {}

    def load_from_csv(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            # Fallback defaults, with reasonable stealth / trail values
            self.add(TravelMode(
                "reckless", "Reckless",
                speed_mod=-1,
                description="Fast movement with risk",
                stealth_dc_mod=+2,      # harder to be stealthy
                trail_type=None,
            ))
            self.add(TravelMode(
                "normal", "Normal",
                speed_mod=0,
                description="Standard travel pace",
                stealth_dc_mod=0,
                trail_type=None,
            ))
            self.add(TravelMode(
                "cautious", "Cautious",
                speed_mod=1,
                description="Slower, stealthier movement",
                stealth_dc_mod=-2,      # easier stealth
                trail_type=None,
            ))
            self.add(TravelMode(
                "exploring", "Exploring",
                speed_mod=2,
                description="Thorough scouting",
                stealth_dc_mod=-1,
                trail_type=None,
            ))
            self.add(TravelMode(
                "trailblazing", "Trailblazing",
                speed_mod=1,
                description="Creates trails while moving",
                stealth_dc_mod=0,
                trail_type="footpath",  # default trail type created
            ))
            return

        with path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                # compatible with your current CSV (no extra columns)
                speed_mod = float(row.get("speed_mod", 0))

                stealth_dc_mod = float(row.get("stealth_dc_mod", 0))
                trail_type = row.get("trail_type")
                if trail_type == "":
                    trail_type = None

                mode = TravelMode(
                    id=row["id"],
                    name=row.get("name", row["id"]),
                    speed_mod=speed_mod,
                    description=row.get("description", ""),
                    stealth_dc_mod=stealth_dc_mod,
                    trail_type=trail_type,
                )
                self.add(mode)

    def add(self, mode: TravelMode):
        self.modes[mode.id] = mode

    def get(self, mid: str) -> TravelMode:
        return self.modes[mid]

    def ids(self):
        return list(self.modes.keys())