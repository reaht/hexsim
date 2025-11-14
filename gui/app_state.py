# file: gui/app_state.py

from dataclasses import dataclass, field
from core.event_bus import EventBus
from core.undo_stack import UndoStack

@dataclass
class AppState:
    grid: any
    biome_lib: any
    party: any
    engine: any
    tools: dict = field(default_factory=dict)
    events: EventBus = field(default_factory=EventBus)
    undo: UndoStack = field(default_factory=UndoStack)