# file: gui/tools/base_tool.py
from gui.app_state import AppState
from typing import Tuple

Coord = Tuple[int, int]


class BaseTool:
    name = "base"

    def on_click(self, coord: Coord, state: AppState):
        pass

    def on_drag(self, coord: Coord, state: AppState):
        pass

    def on_release(self, state: AppState):
        pass