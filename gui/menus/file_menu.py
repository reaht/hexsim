# file: gui/menus/file_menu.py
import tkinter as tk
from tkinter import filedialog, messagebox
import json

from gui.app_state import AppState
from core.grid import HexGrid


class FileMenu:
    """
    Owns the File menu (Save Map / Load Map).
    Ensures a menubar exists so EditMenu can attach to it.
    """

    def __init__(self, root: tk.Tk, state: AppState):
        self.root = root
        self.state = state

        # Attach or create menubar
        menubar = root.nametowidget(root.cget("menu")) if root.cget("menu") else None
        if menubar is None:
            menubar = tk.Menu(root)
            root.config(menu=menubar)

        self.menubar = menubar

        # Build File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="Save Map", command=self.save_map)
        self.filemenu.add_command(label="Load Map", command=self.load_map)

    # ---------------------------------------------------------
    # Actions
    # ---------------------------------------------------------
    def save_map(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        with open(path, "w") as f:
            json.dump(self.state.grid.to_dict(), f, indent=2)

        messagebox.showinfo("Saved", "Map saved.")

    def load_map(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        with open(path) as f:
            data = json.load(f)

        new_grid = HexGrid.from_dict(data)
        new_grid.biome_lib = self.state.biome_lib

        # Swap into state + engine
        self.state.grid = new_grid
        self.state.engine.grid = new_grid

        # Reset undo history as requested
        self.state.undo.clear()

        # Notify the system
        self.state.events.publish("map_loaded")
        self.state.events.publish("grid_changed")

        messagebox.showinfo("Loaded", "Map loaded.")