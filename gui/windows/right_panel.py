# file: gui/windows/right_panel.py
from tkinter import ttk
from gui.ui.movement_panel import MovementPanel


class RightPanel:
    """
    Pure UI view for movement & time controls.
    """

    def __init__(self, parent, state):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side="left", fill="y")

        self.movement_panel = MovementPanel(self.frame, state)