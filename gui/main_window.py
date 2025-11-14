# file: gui/main_window.py
import tkinter as tk
from tkinter import ttk

from gui.app_state import AppState

from gui.windows.left_panel import LeftPanel
from gui.windows.left_panel_controller import LeftPanelController

from gui.windows.center_panel import CenterPanel
from gui.windows.center_panel_controller import CenterPanelController

from gui.windows.right_panel import RightPanel

from gui.menus.file_menu import FileMenu
from gui.menus.edit_menu import EditMenu

from gui.input.shortcuts import bind_shortcuts


class MainWindow:
    def __init__(self, root, state: AppState):
        self.root = root
        self.state = state

        # Layout frames
        self._build_frames()

        # Build panels + controllers
        self.left_view = LeftPanel(self.left_frame)
        self.left_controller = LeftPanelController(self.left_view, state)

        self.center_view = CenterPanel(self.center_frame, state.grid)
        self.center_controller = CenterPanelController(self.center_view, state)

        self.right_view = RightPanel(self.right_frame, state)

        # Menus
        FileMenu(root, state)
        EditMenu(root, state)

        # Shortcuts
        bind_shortcuts(root, state)

        # Initial redraw
        state.events.publish("party_moved", state.party.position)
        state.events.publish("grid_changed")

    def _build_frames(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y")

        self.center_frame = ttk.Frame(self.main_frame)
        self.center_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="left", fill="y")