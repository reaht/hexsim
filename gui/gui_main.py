# file: gui/gui_main.py
import tkinter as tk
from tkinter import filedialog, messagebox

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from simulation.engine import SimulationEngine

from gui.app_state import AppState
from gui.main_window import MainWindow


def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator")

    # ---------------------------------------------------------
    # Load biome definitions
    # ---------------------------------------------------------
    biome_lib = BiomeLibrary()
    biome_lib.load_from_csv("config/biomes.csv")

    # ---------------------------------------------------------
    # Create base grid
    # ---------------------------------------------------------
    grid = HexGrid()
    grid.biome_lib = biome_lib
    grid.generate_rectangle(15, 15, default_biome="plains")

    # ---------------------------------------------------------
    # Load party
    # ---------------------------------------------------------
    party = load_party_from_csv("config/party.csv", leader_index=0, start_pos=(0, 0))

    # ---------------------------------------------------------
    # Simulation Engine
    # ---------------------------------------------------------
    engine = SimulationEngine(grid, party)

    # ---------------------------------------------------------
    # Global App State
    # ---------------------------------------------------------
    state = AppState(
        grid=grid,
        biome_lib=biome_lib,
        party=party,
        engine=engine,
    )

    # ---------------------------------------------------------
    # Launch Main Window
    # ---------------------------------------------------------
    MainWindow(root, state)

    # ---------------------------------------------------------
    # Enter main loop
    # ---------------------------------------------------------
    root.mainloop()