# file: gui/ui/movement_panel.py
import tkinter as tk
from tkinter import ttk

from core.command import MovePartyCommand
from core.movement import AXIAL_DIRECTIONS, add


class MovementPanel:
    """
    Right-side movement system using:
      - CSV-driven travel modes
      - token/exhaustion tracking
      - undoable party movement (MovePartyCommand)
      - engine cost resolution
    """

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

        # Travel mode variable from AppState
        self.mode_var = state.travel_mode_var

        self.time_label = None
        self.status_frame = None

        self._build()

        # Listen for updates when movement occurs
        state.events.subscribe("party_moved", self._refresh_time)
        state.events.subscribe("party_moved", self._refresh_status)

    # ---------------------------------------------------------
    # UI layout
    # ---------------------------------------------------------
    def _build(self):
        ttk.Label(self.parent, text="Movement").pack(pady=5)

        grid_frame = ttk.Frame(self.parent)
        grid_frame.pack(pady=10)

        # Hex-direction buttons
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
                grid_frame,
                text=label,
                command=lambda i=idx: self._move(i),
            ).grid(row=row, column=col)

        # Travel mode dropdown (CSV-driven)
        ttk.Label(self.parent, text="Travel Mode").pack(pady=5)

        mode_box = ttk.Combobox(
            self.parent,
            textvariable=self.mode_var,
            values=self.state.travel_modes.ids(),
            state="readonly",
        )
        mode_box.pack(pady=4)

        # Time token display
        self.time_label = ttk.Label(self.parent, text="Time: 0.00 days")
        self.time_label.pack(pady=8)

        # Token + exhaustion display
        self.status_frame = ttk.Frame(self.parent)
        self.status_frame.pack(pady=8, fill="x")

        self._refresh_status()

    # ---------------------------------------------------------
    # Movement logic (undoable)
    # ---------------------------------------------------------
    def _move(self, direction_index: int):
        state = self.state
        party = state.party
        engine = state.engine
        grid = state.grid

        src = party.position
        dq, dr = AXIAL_DIRECTIONS[direction_index]
        dst = add(src, (dq, dr))

        if not grid.has(dst):
            return   # Cannot move off the map

        mode_id = self.mode_var.get()

        # Engine returns (dst, cost)
        result = engine.move_dir(direction_index, mode_id)
        if result is None:
            return

        dst, cost = result

        # Apply cost BEFORE movement (rules: you pay the moment you choose to move)
        engine.apply_movement_cost(cost)

        # Make movement undoable (this ONLY moves the leader/party position)
        cmd = MovePartyCommand(src, dst)

        state.undo.begin()
        state.undo.add(cmd)
        state.undo.commit(state)

        # Notify rest of GUI
        state.events.publish("party_moved", dst)
        state.events.publish("grid_changed")

    # ---------------------------------------------------------
    # UI Updates
    # ---------------------------------------------------------
    def _refresh_time(self, *_):
        """Update world time display."""
        days = self.state.engine.get_time()
        self.time_label.config(text=f"Time: {days:.2f} days")

    def _refresh_status(self, *_):
        """Update token/exhaustion panel for each party member."""
        frame = self.status_frame

        # Clear old rows
        for c in frame.winfo_children():
            c.destroy()

        ttk.Label(frame, text="Party Status:").pack(anchor="w")

        for m in self.state.party.members:
            ttk.Label(
                frame,
                text=(
                    f"{m.name}: "
                    f"{m.tokens:.1f}/{m.max_tokens} tokens,  "
                    f"Exhaustion {m.exhaustion:.1f}"
                ),
            ).pack(anchor="w")