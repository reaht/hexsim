# file: gui/app_state.py

from dataclasses import dataclass, field
import tkinter as tk

from core.event_bus import EventBus
from gui.undo_manager import UndoManager   # your GUI-undo class


@dataclass
class AppState:
    grid: any
    biome_lib: any
    party: any
    engine: any

    # Tools will be injected by LeftPanelController
    tools: dict = field(default_factory=dict)

    # Global event bus
    events: EventBus = field(default_factory=EventBus)

    # Undo/redo manager
    undo: UndoManager = field(default_factory=UndoManager)

    # 🔥 Add this: a globally shared selected tool variable
    current_tool_var: tk.StringVar = field(
        default_factory=lambda: tk.StringVar(value="select")
    )

    current_trail_var: tk.StringVar = field(
        default_factory=lambda: tk.StringVar(value="footpath")
    )