# file: gui/ui/file_menu.py
import tkinter as tk
from tkinter import filedialog, messagebox
import json

from gui.app_state import AppState
from core.grid import HexGrid


class FileMenu:
    """
    Creates/owns the File menu (Save Map / Load Map).

    Also ensures there is a menubar on the root window that EditMenu can
    attach to.
    """

    def __init__(self, root: tk.Tk, state: AppState):
        self.root = root
        self.state = state

        # Get or create the menubar
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

        # Swap grids in state and engine
        self.state.grid = new_grid
        self.state.engine.grid = new_grid

        # Clear undo/redo history on load (as requested)
        self.state.undo.clear()

        # Notify the rest of the system
        self.state.events.publish("map_loaded")
        self.state.events.publish("grid_changed")

        messagebox.showinfo("Loaded", "Map loaded.")


class EditMenu:
    """
    Edit menu: Undo / Redo items.

    Note: keyboard shortcuts are bound in MainWindow; this just exposes
    menu entries that call the same undo/redo actions.
    """

    def __init__(self, root: tk.Tk, state: AppState):
        self.root = root
        self.state = state

        # Reuse existing menubar created by FileMenu
        menubar = root.nametowidget(root.cget("menu")) if root.cget("menu") else None
        if menubar is None:
            menubar = tk.Menu(root)
            root.config(menu=menubar)

        self.menubar = menubar

        self.editmenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.editmenu.add_command(
            label="Undo",
            accelerator="Ctrl+Z",
            command=self._do_undo,
        )
        self.editmenu.add_command(
            label="Redo",
            accelerator="Ctrl+Y",
            command=self._do_redo,
        )

    def _do_undo(self):
        self.state.undo.undo(self.state)

    def _do_redo(self):
        self.state.undo.redo(self.state)