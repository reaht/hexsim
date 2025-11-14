# file: gui/app_state.py
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AppState:
    """
    Shared application state for the hexcrawl GUI.

    Keeps references to core simulation objects and the tools dictionary.
    Concrete types are kept as Any to avoid import cycles.
    """
    grid: Any
    biome_lib: Any
    party: Any
    engine: Any
    tools: Dict[str, Any] = field(default_factory=dict)