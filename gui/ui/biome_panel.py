# file: gui/ui/biome_panel.py
import tkinter as tk
from tkinter import ttk
from typing import List


class BiomePanel:
    """
    Biome selection UI: just a label + combobox.
    Tools that need biome info (PaintBiomeTool) use biome_var.
    """

    def __init__(self, parent, biome_ids: List[str]):
        self.parent = parent
        self.biome_ids = biome_ids
        self.biome_var = tk.StringVar(value=biome_ids[0] if biome_ids else "")

        self._build()

    def _build(self):
        ttk.Label(self.parent, text="Biome", font=("Arial", 10, "bold")).pack(pady=6)

        self.combo = ttk.Combobox(
            self.parent,
            textvariable=self.biome_var,
            values=self.biome_ids,
            state="readonly",
        )
        self.combo.pack(pady=4)