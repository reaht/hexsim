# file: gui/app_state.py

from dataclasses import dataclass, field

from core.event_bus import EventBus
from gui.undo_manager import UndoManager   # CHANGED — now uses GUI version


@dataclass
class AppState:
    grid: any
    biome_lib: any
    party: any
    engine: any

    tools: dict = field(default_factory=dict)
    events: EventBus = field(default_factory=EventBus)
    undo: UndoManager = field(default_factory=UndoManager)   # CHANGED