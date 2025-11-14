# file: gui/ui/movement_panel.py

import tkinter as tk
from tkinter import ttk

from core.command import MovePartyCommand
from core.movement import AXIAL_DIRECTIONS, add, calculate_time_cost


class MovementPanel:
    """
    Right-side movement panel using the new undo/redo architecture.
    """

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

        self.speed_var = tk.StringVar(value="normal")
        self.time_label = None

        self._build()

        # update time when party moves
        state.events.subscribe("party_moved", self._update_time)

    # ---------------------------------------------------------
    # UI layout
    # ---------------------------------------------------------

    def _build(self):
        ttk.Label(self.parent, text="Movement").pack(pady=5)

        mvf = ttk.Frame(self.parent)
        mvf.pack(pady=10)

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
                command=lambda i=idx: self._move(i),
            ).grid(row=row, column=col)

        ttk.Label(self.parent, text="Speed Mode").pack(pady=5)
        ttk.Combobox(
            self.parent,
            textvariable=self.speed_var,
            values=["cautious", "normal", "fast"],
            state="readonly",
        ).pack(pady=4)

        self.time_label = ttk.Label(self.parent, text="Time Tokens: 0.00")
        self.time_label.pack(pady=8)

    # ---------------------------------------------------------
    # Movement logic (undoable)
    # ---------------------------------------------------------

    def _move(self, direction_index: int):
        state = self.state
        grid = state.grid
        party = state.party
        engine = state.engine

        src = party.position
        dq, dr = AXIAL_DIRECTIONS[direction_index]
        dst = add(src, (dq, dr))

        # out of bounds
        if not grid.has(dst):
            return

        mode = self.speed_var.get()
        cost = calculate_time_cost(party, grid, src, dst, mode)

        # make undoable command
        cmd = MovePartyCommand(src, dst)

        # push to undo system
        state.undo.begin()
        state.undo.add(cmd)
        state.undo.commit(state)

        # time accumulation
        engine.scheduler.advance(cost)

        # event bus updates all views
        state.events.publish("party_moved", dst)
        state.events.publish("grid_changed")

        # update the label locally too
        self._update_time()

    # ---------------------------------------------------------
    # UI update helpers
    # ---------------------------------------------------------

    def _update_time(self, *_):
        self.time_label.config(
            text=f"Time Tokens: {self.state.engine.scheduler.time_tokens:.2f}"
        )