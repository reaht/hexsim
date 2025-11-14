# file: gui/gui_main.py
import tkinter as tk

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from simulation.engine import SimulationEngine

from gui.app_state import AppState
from gui.main_window import MainWindow


def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator")

    biome_lib = BiomeLibrary()
    biome_lib.load_from_csv("config/biomes.csv")

    grid = HexGrid()
    grid.biome_lib = biome_lib
    grid.generate_rectangle(15, 15, default_biome="plains")

    party = load_party_from_csv("config/party.csv", leader_index=0, start_pos=(0, 0))
    engine = SimulationEngine(grid, party)

    state = AppState(
        grid=grid,
        biome_lib=biome_lib,
        party=party,
        engine=engine,
    )

    MainWindow(root, state)

    root.mainloop()