# file: gui/app_state.py
from dataclasses import dataclass, field
from typing import Any, Dict

from core.event_bus import EventBus


@dataclass
class AppState:
    """
    Shared application state for the hexcrawl GUI.

    Holds references to:
      - grid
      - biome library
      - party
      - engine
      - tools
      - global event bus
    """
    grid: Any
    biome_lib: Any
    party: Any
    engine: Any
    tools: Dict[str, Any] = field(default_factory=dict)
    events: EventBus = field(default_factory=EventBus)