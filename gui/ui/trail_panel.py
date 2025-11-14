# file: gui/ui/trail_panel.py
import tkinter as tk
from tkinter import ttk


class TrailPanel:
    def __init__(self, parent, trail_ids):
        self.frame = ttk.LabelFrame(parent, text="Trail Types")
        self.frame.pack(fill="x", padx=4, pady=4)

        self.trail_var = tk.StringVar(value=trail_ids[0])

        ttk.Label(self.frame, text="Trail:").pack(anchor="w")
        ttk.Combobox(
            self.frame,
            textvariable=self.trail_var,
            values=trail_ids,
            state="readonly",
        ).pack(fill="x", pady=2)