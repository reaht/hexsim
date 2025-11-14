# file: gui/ui/toolbar.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class Toolbar:
    """
    Left-side tool palette + Undo / Redo controls.
    """

    def __init__(self, parent, tools: Dict[str, Any], current_tool_var: tk.StringVar, state):
        """
        parent: parent Tk frame
        tools: dict of tool_id -> tool_instance
        current_tool_var: StringVar storing the selected tool ID
        state: AppState (provides undo/redo functionality)
        """
        self.parent = parent
        self.tools = tools
        self.state = state
        self.current_tool_var = current_tool_var

        self.buttons: Dict[str, ttk.Button] = {}
        self.history_buttons: Dict[str, ttk.Button] = {}

        self._build()

    # ---------------------------------------------------------
    # Build UI
    # ---------------------------------------------------------
    def _build(self):
        # =========== Tool Section ===========
        ttk.Label(self.parent, text="Tools", font=("Arial", 11, "bold")).pack(pady=4)

        def add_tool_button(label: str, tool_id: str):
            btn = ttk.Button(
                self.parent,
                text=label,
                width=20,
                command=lambda: self.set_tool(tool_id),
            )
            btn.pack(pady=2)
            self.buttons[tool_id] = btn

        add_tool_button("Select", "select")
        add_tool_button("Paint Biome", "paint_biome")
        add_tool_button("Paint Trail", "paint_trail")
        add_tool_button("Erase Trail", "erase_trail")
        add_tool_button("Inspect", "inspect")

        self._update_button_styles()

        # =========== Separator ===========
        ttk.Separator(self.parent, orient="horizontal").pack(fill="x", pady=10)

        # =========== Undo/Redo Section ===========
        ttk.Label(self.parent, text="History", font=("Arial", 10, "bold")).pack(pady=4)

        undo_btn = ttk.Button(
            self.parent,
            text="Undo (Ctrl+Z)",
            width=20,
            command=self._do_undo
        )
        undo_btn.pack(pady=2)
        self.history_buttons["undo"] = undo_btn

        redo_btn = ttk.Button(
            self.parent,
            text="Redo (Ctrl+Y)",
            width=20,
            command=self._do_redo
        )
        redo_btn.pack(pady=2)
        self.history_buttons["redo"] = redo_btn

    # ---------------------------------------------------------
    # Tool Selection
    # ---------------------------------------------------------
    def set_tool(self, tool_id: str):
        if tool_id not in self.tools:
            return
        self.current_tool_var.set(tool_id)
        self._update_button_styles()

    def _update_button_styles(self):
        active = self.current_tool_var.get()
        for tid, btn in self.buttons.items():
            if tid == active:
                btn.state(["pressed"])
            else:
                btn.state(["!pressed"])

    # ---------------------------------------------------------
    # Undo / Redo
    # ---------------------------------------------------------
    def _do_undo(self):
        self.state.undo.undo(self.state)

    def _do_redo(self):
        self.state.undo.redo(self.state)