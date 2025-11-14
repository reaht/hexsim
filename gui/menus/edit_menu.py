# file: gui/menus/edit_menu.py
import tkinter as tk
from gui.app_state import AppState


class EditMenu:
    """
    Edit menu: Undo / Redo entries.
    Keyboard shortcuts are bound in MainWindow.
    """

    def __init__(self, root: tk.Tk, state: AppState):
        self.root = root
        self.state = state

        # Attach or create menubar (FileMenu usually created it already)
        menubar = root.nametowidget(root.cget("menu")) if root.cget("menu") else None
        if menubar is None:
            menubar = tk.Menu(root)
            root.config(menu=menubar)

        self.menubar = menubar

        # Build Edit menu
        self.editmenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.editmenu.add_command(
            label="Undo",
            accelerator="Ctrl+Z",
            command=self._do_undo
        )
        self.editmenu.add_command(
            label="Redo",
            accelerator="Ctrl+Y",
            command=self._do_redo
        )

    def _do_undo(self):
        self.state.undo.undo(self.state)

    def _do_redo(self):
        self.state.undo.redo(self.state)