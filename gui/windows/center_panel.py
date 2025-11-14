# file: gui/windows/center_panel.py
import tkinter as tk
from tkinter import ttk

from gui.grid_widget import HexGridWidget


class CenterPanel:
    """
    Pure UI view for the central hex grid editor.
    The controller handles all interaction.
    """
    def __init__(self, parent, grid, cell_size=32):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side="left", fill="both", expand=True)

        self.grid_widget = HexGridWidget(
            self.frame, grid, cell_size=cell_size, bg="white"
        )
        self.grid_widget.pack(fill="both", expand=True)