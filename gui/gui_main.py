# file: gui/gui_main.py
import tkinter as tk
from tkinter import filedialog, messagebox

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from simulation.engine import SimulationEngine

from gui.app_state import AppState
from gui.main_window import MainWindow

from core.trail_type import TrailLibrary

def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator")

    # --- Load biomes ---
    biome_lib = BiomeLibrary()
    biome_lib.load_from_csv("config/biomes.csv")

    # --- Load trails ---
    trail_lib = TrailLibrary()
    trail_lib.load_from_csv("config/trails.csv")

    # --- Create grid ---
    grid = HexGrid()
    grid.biome_lib = biome_lib
    grid.trail_lib = trail_lib     # ✅ now safe — grid exists
    grid.generate_rectangle(15, 15, default_biome="plains")

    # --- Party ---
    party = load_party_from_csv("config/party.csv", leader_index=0, start_pos=(0, 0))

    # --- Engine ---
    engine = SimulationEngine(grid, party)

    # --- App state ---
    state = AppState(
        grid=grid,
        biome_lib=biome_lib,
        party=party,
        engine=engine,
    )

    MainWindow(root, state)
    root.mainloop()