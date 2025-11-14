# file: gui/windows/left_panel.py
import tkinter as tk
from tkinter import ttk

from gui.ui.toolbar import Toolbar
from gui.ui.biome_panel import BiomePanel
from gui.ui.trail_panel import TrailPanel


class LeftPanel:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side="left", fill="y")

        self.toolbar_area = ttk.Frame(self.frame)
        self.toolbar_area.pack(fill="x", pady=4)

        self.biome_area = ttk.Frame(self.frame)
        self.biome_area.pack(fill="x", pady=4)

        self.trail_area = ttk.Frame(self.frame)      # ✅ ADD THIS
        self.trail_area.pack(fill="x", pady=4)

        self.toolbar = None
        self.biome_panel = None
        self.trail_panel = None                      # ✅ ADD THIS