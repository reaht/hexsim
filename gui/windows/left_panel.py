# file: gui/windows/left_panel.py
import tkinter as tk
from tkinter import ttk

from gui.ui.toolbar import Toolbar
from gui.ui.biome_panel import BiomePanel


class LeftPanel:
    """
    Pure UI container.
    Contains:
      - Toolbar buttons
      - Biome panel (biome picker)
    """
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side="left", fill="y")

        self.toolbar_area = ttk.Frame(self.frame)
        self.toolbar_area.pack(fill="x", pady=4)

        self.biome_area = ttk.Frame(self.frame)
        self.biome_area.pack(fill="x", pady=4)

        # Subviews (filled by controller)
        self.toolbar: Toolbar | None = None
        self.biome_panel: BiomePanel | None = None