# file: gui/ui/file_menu.py
import tkinter as tk
from tkinter import filedialog, messagebox
import json

from gui.app_state import AppState
from gui.grid_widget import HexGridWidget
from core.grid import HexGrid


class FileMenu:
    """
    Adds File menu with save/load map actions.
    """

    def __init__(self, root: tk.Tk, state: AppState, grid_widget: HexGridWidget):
        self.root = root
        self.state = state
        self.grid_widget = grid_widget

        self._build_menu()

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="Save Map", command=self.save_map)
        filemenu.add_command(label="Load Map", command=self.load_map)

    def save_map(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return

        with open(path, "w") as f:
            json.dump(self.state.grid.to_dict(), f, indent=2)

        messagebox.showinfo("Saved", "Map saved.")

    def load_map(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return

        with open(path) as f:
            data = json.load(f)

        new_grid = HexGrid.from_dict(data)
        new_grid.biome_lib = self.state.biome_lib

        # Swap into state + widget + engine
        self.state.grid = new_grid
        self.state.engine.grid = new_grid
        self.grid_widget.grid = new_grid
        self.grid_widget._compute_canvas_size()
        self.grid_widget.redraw()

        messagebox.showinfo("Loaded", "Map loaded.")