# file: gui/gui_main.py
import tkinter as tk

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from core.trail_type import TrailLibrary
from core.travel_modes import TravelModeLibrary

from simulation.engine import SimulationEngine

from gui.app_state import AppState
from gui.main_window import MainWindow


def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator")

    # ---------------------------------------------------------
    # Biome definitions
    # ---------------------------------------------------------
    biome_lib = BiomeLibrary()
    biome_lib.load_from_csv("config/biomes.csv")

    # ---------------------------------------------------------
    # Trail types
    # ---------------------------------------------------------
    trail_lib = TrailLibrary()
    trail_lib.load_from_csv("config/trails.csv")

    # ---------------------------------------------------------
    # Travel modes (new)
    # ---------------------------------------------------------
    travel_modes = TravelModeLibrary()
    travel_modes.load_from_csv("config/travel_modes.csv")

    # ---------------------------------------------------------
    # Create grid
    # ---------------------------------------------------------
    grid = HexGrid()
    grid.biome_lib = biome_lib
    grid.trail_lib = trail_lib
    grid.generate_rectangle(15, 15, default_biome="plains")

    # ---------------------------------------------------------
    # Party
    # ---------------------------------------------------------
    party = load_party_from_csv(
        "config/party.csv",
        leader_index=0,
        start_pos=(0, 0)
    )

    # ---------------------------------------------------------
    # Simulation Engine  ← FIXED: pass travel_modes
    # ---------------------------------------------------------
    engine = SimulationEngine(grid, party, travel_modes)

    # ---------------------------------------------------------
    # App State
    # ---------------------------------------------------------
    state = AppState(
        grid=grid,
        biome_lib=biome_lib,
        party=party,
        engine=engine,
    )

    # Attach travel modes to state for the MovementPanel
    state.travel_modes = travel_modes
    state.travel_mode_var = tk.StringVar(value="normal")

    # ---------------------------------------------------------
    # Launch main window
    # ---------------------------------------------------------
    MainWindow(root, state)

    root.mainloop()