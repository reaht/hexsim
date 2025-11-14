# file: gui/ui/movement_panel.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

from gui.app_state import AppState
from gui.grid_widget import HexGridWidget


class MovementPanel:
    """
    Right-side movement controls:
      - Direction buttons
      - Speed mode dropdown
      - Time token display
    """

    def __init__(self, parent, state: AppState, grid_widget: HexGridWidget):
        self.parent = parent
        self.state = state
        self.grid_widget = grid_widget

        self.speed_var = tk.StringVar(value="normal")
        self.time_label = None

        self._build()

    def _build(self):
        ttk.Label(self.parent, text="Movement").pack(pady=5)

        mvf = ttk.Frame(self.parent)
        mvf.pack(pady=10)

        def do_move(idx: int):
            mode = self.speed_var.get()
            if self.state.engine.move_dir(idx, mode):
                # Update party position on the map
                self.grid_widget.set_party_positions([self.state.party.position])
                self.grid_widget.redraw()
                self.time_label.config(
                    text=f"Time Tokens: {self.state.engine.get_time():.2f}"
                )

        # Direction buttons in hex layout
        buttons = [
            ("N", 0, 0, 1),
            ("NW", 5, 1, 0),
            ("NE", 1, 1, 2),
            ("SW", 4, 2, 0),
            ("SE", 2, 2, 2),
            ("S", 3, 3, 1),
        ]
        for label, idx, row, col in buttons:
            ttk.Button(
                mvf,
                text=label,
                command=lambda i=idx: do_move(i),
            ).grid(row=row, column=col)

        # Speed mode dropdown
        ttk.Label(self.parent, text="Speed Mode").pack(pady=5)
        ttk.Combobox(
            self.parent,
            textvariable=self.speed_var,
            values=["cautious", "normal", "fast"],
            state="readonly",
        ).pack(pady=4)

        # Time label
        self.time_label = ttk.Label(self.parent, text="Time Tokens: 0.00")
        self.time_label.pack(pady=8)