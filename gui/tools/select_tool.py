# file: gui/tools/select_tool.py
from typing import Tuple
from tkinter import messagebox

from gui.tools.base_tool import BaseTool
from gui.app_state import AppState

Coord = Tuple[int, int]


class SelectTool(BaseTool):
    name = "select"

    def on_click(self, coord: Coord, state: AppState):
        # Move party to clicked hex
        if coord not in state.grid.tiles:
            return
        state.party.position = coord
        state.events.publish("party_moved", coord)
        state.events.publish("grid_changed")