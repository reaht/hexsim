# file: gui/ui/toolbar.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class Toolbar:
    """
    Left-side tool palette (Select, Paint Biome, Paint Trail, etc.)
    """

    def __init__(self, parent, tools: Dict[str, Any], current_tool_var: tk.StringVar):
        self.parent = parent
        self.tools = tools
        self.current_tool_var = current_tool_var
        self.buttons: Dict[str, ttk.Button] = {}

        self._build()

    def _build(self):
        ttk.Label(self.parent, text="Tools", font=("Arial", 11, "bold")).pack(pady=4)

        def add_button(label: str, tool_id: str):
            btn = ttk.Button(
                self.parent,
                text=label,
                width=20,
                command=lambda: self.set_tool(tool_id),
            )
            btn.pack(pady=2)
            self.buttons[tool_id] = btn

        add_button("Select", "select")
        add_button("Paint Biome", "paint_biome")
        add_button("Paint Trail", "paint_trail")
        add_button("Erase Trail", "erase_trail")
        add_button("Inspect", "inspect")

        # initial highlighting
        self._update_button_styles()

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