# file: gui/gui_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from simulation.engine import SimulationEngine
from gui.grid_widget import HexGridWidget
from core.movement import AXIAL_DIRECTIONS  # NEW: to compute direction between hexes


# ---------------------------------------------------------
# Tool identifiers (like Photoshop tools)
# ---------------------------------------------------------
TOOL_SELECT = "select"
TOOL_PAINT_BIOME = "paint_biome"
TOOL_PAINT_TRAIL = "paint_trail"
TOOL_ERASE_TRAIL = "erase_trail"
TOOL_INSPECT = "inspect"


def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator (Axial Dictionary Grid)")

    # ---------------------------------------------------------
    # Load biome library
    # ---------------------------------------------------------
    biome_lib = BiomeLibrary()
    biome_lib.load_from_csv("config/biomes.csv")

    # ---------------------------------------------------------
    # Create grid
    # ---------------------------------------------------------
    grid = HexGrid()
    grid.biome_lib = biome_lib
    grid.generate_rectangle(15, 15, default_biome="plains")

    # ---------------------------------------------------------
    # Load party
    # ---------------------------------------------------------
    party = load_party_from_csv("config/party.csv", leader_index=0, start_pos=(0, 0))

    # ---------------------------------------------------------
    # Engine
    # ---------------------------------------------------------
    engine = SimulationEngine(grid, party)

    # Track last coord for auto-direction trail brush
    trail_last_coord: list[tuple[int, int] | None] = [None]

    # ---------------------------------------------------------
    # Layout frames
    # ---------------------------------------------------------
    main = ttk.Frame(root)
    main.pack(fill="both", expand=True)

    left = ttk.Frame(main)
    left.pack(side="left", fill="y")

    center = ttk.Frame(main)
    center.pack(side="left", fill="both", expand=True)

    right = ttk.Frame(main)
    right.pack(side="left", fill="y")

    # ---------------------------------------------------------
    # Toolbar
    # ---------------------------------------------------------
    ttk.Label(left, text="Tools", font=("Arial", 11, "bold")).pack(pady=4)

    current_tool = tk.StringVar(value=TOOL_SELECT)

    def make_tool_button(text, tool_id):
        btn = ttk.Button(left, text=text, width=20,
                         command=lambda: current_tool.set(tool_id))
        btn.pack(pady=2)
        return btn

    btn_select = make_tool_button("Select", TOOL_SELECT)
    btn_biome = make_tool_button("Paint Biome", TOOL_PAINT_BIOME)
    btn_trail = make_tool_button("Paint Trail", TOOL_PAINT_TRAIL)
    btn_erase = make_tool_button("Erase Trail", TOOL_ERASE_TRAIL)
    btn_inspect = make_tool_button("Inspect", TOOL_INSPECT)

    # ---------------------------------------------------------
    # Subpanel: Biome selection (only used by paint_biome tool)
    # ---------------------------------------------------------
    ttk.Label(left, text="Biome", font=("Arial", 10, "bold")).pack(pady=5)

    biome_ids = biome_lib.ids()
    biome_var = tk.StringVar(value=biome_ids[0])

    biome_box = ttk.Combobox(left, textvariable=biome_var,
                             values=biome_ids, state="readonly")
    biome_box.pack(pady=4)

    # (Trail direction dropdown removed – we now auto-detect direction while dragging)

    # ---------------------------------------------------------
    # Grid display
    # ---------------------------------------------------------
    grid_widget = HexGridWidget(center, grid, cell_size=32, bg="white")
    grid_widget.pack(fill="both", expand=True)

    biome_colors = {
        "plains": "#b7e590",
        "forest": "#4c9a2a",
        "mountain": "#b0b0b0",
        "swamp": "#5b7e5a",
    }
    grid_widget.set_biome_colors(biome_colors)
    grid_widget.set_party_positions([party.position])

    # ---------------------------------------------------------
    # On-click behavior (all tools funnel through here)
    # ---------------------------------------------------------
    def on_hex_clicked(coord):
        tile = grid.get(coord)
        tool = current_tool.get()

        # If we're not in trail-paint tool, reset the brush start
        if tool != TOOL_PAINT_TRAIL:
            trail_last_coord[0] = None

        if tool == TOOL_PAINT_BIOME:
            grid.set_biome(coord, biome_var.get())
            grid_widget.redraw()
            return

        if tool == TOOL_PAINT_TRAIL:
            prev = trail_last_coord[0]

            # First hex in a stroke: just remember and wait for drag
            if prev is None:
                trail_last_coord[0] = coord
                return

            # Same hex → nothing to do
            if prev == coord:
                return

            dq = coord[0] - prev[0]
            dr = coord[1] - prev[1]

            # Find which of the 6 directions this movement is
            dir_idx = None
            for i, (adq, adr) in enumerate(AXIAL_DIRECTIONS):
                if (adq, adr) == (dq, dr):
                    dir_idx = i
                    break

            if dir_idx is None:
                # Not adjacent — treat this as a new starting point
                trail_last_coord[0] = coord
                return

            # Set bidirectional trail from prev to coord
            grid.set_trail(prev, dir_idx, True)
            trail_last_coord[0] = coord
            grid_widget.redraw()
            return

        if tool == TOOL_ERASE_TRAIL:
            for i in range(6):
                grid.set_trail(coord, i, False)
            grid_widget.redraw()
            return

        if tool == TOOL_INSPECT:
            messagebox.showinfo(
                "Hex Info",
                f"Coord: {coord}\nBiome: {tile.biome_id}\nTrails: {tile.trails}"
            )
            return

        # TOOL_SELECT (or default) → move party
        party.position = coord
        grid_widget.set_party_positions([party.position])
        grid_widget.redraw()

    grid_widget.set_on_hex_clicked(on_hex_clicked)

    # ---------------------------------------------------------
    # Movement UI
    # ---------------------------------------------------------
    ttk.Label(right, text="Movement").pack(pady=5)

    def do_move(idx):
        mode = speed_var.get()
        if engine.move_dir(idx, mode):
            grid_widget.set_party_positions([party.position])
            grid_widget.redraw()
            time_label.config(text=f"Time Tokens: {engine.get_time():.2f}")

    mvf = ttk.Frame(right)
    mvf.pack(pady=10)

    ttk.Button(mvf, text="N", command=lambda: do_move(0)).grid(row=0, column=1)
    ttk.Button(mvf, text="NW", command=lambda: do_move(5)).grid(row=1, column=0)
    ttk.Button(mvf, text="NE", command=lambda: do_move(1)).grid(row=1, column=2)
    ttk.Button(mvf, text="SW", command=lambda: do_move(4)).grid(row=2, column=0)
    ttk.Button(mvf, text="SE", command=lambda: do_move(2)).grid(row=2, column=2)
    ttk.Button(mvf, text="S", command=lambda: do_move(3)).grid(row=3, column=1)

    ttk.Label(right, text="Speed Mode").pack(pady=5)
    speed_var = tk.StringVar(value="normal")
    ttk.Combobox(right, textvariable=speed_var,
                 values=["cautious", "normal", "fast"], state="readonly").pack(pady=4)

    time_label = ttk.Label(right, text="Time Tokens: 0.00")
    time_label.pack(pady=10)

    # ---------------------------------------------------------
    # File menu
    # ---------------------------------------------------------
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    filemenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="File", menu=filemenu)

    def save_map():
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w") as f:
            json.dump(grid.to_dict(), f, indent=2)
        messagebox.showinfo("Saved", "Map saved.")

    def load_map():
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path) as f:
            data = json.load(f)
        new_grid = HexGrid.from_dict(data)
        new_grid.biome_lib = biome_lib
        engine.grid = new_grid
        grid_widget.grid = new_grid
        grid_widget.redraw()
        messagebox.showinfo("Loaded", "Map loaded.")

    filemenu.add_command(label="Save Map", command=save_map)
    filemenu.add_command(label="Load Map", command=load_map)

    root.mainloop()