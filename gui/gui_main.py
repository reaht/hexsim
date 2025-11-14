# file: gui/gui_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

from core.biome import BiomeLibrary
from core.grid import HexGrid
from core.party import load_party_from_csv
from simulation.engine import SimulationEngine

from gui.grid_widget import HexGridWidget

# Tools
from gui.tools.select_tool import SelectTool
from gui.tools.inspect_tool import InspectTool
from gui.tools.paint_biome_tool import PaintBiomeTool
from gui.tools.paint_trail_tool import PaintTrailTool
from gui.tools.erase_trail_tool import EraseTrailTool


def run_app():
    root = tk.Tk()
    root.title("Hexcrawl Simulator")

    # ---------------------------------------------------------
    # Load biomes
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

    # ---------------------------------------------------------
    # Layout
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

    biome_ids = biome_lib.ids()
    biome_var = tk.StringVar(value=biome_ids[0])

    tools = {
        "select": SelectTool(),
        "inspect": InspectTool(),
        "paint_biome": PaintBiomeTool(biome_var),
        "paint_trail": PaintTrailTool(),
        "erase_trail": EraseTrailTool(),
    }

    current_tool = tk.StringVar(value="select")

    def set_tool(t):
        current_tool.set(t)

    def tool_button(name, tool_id):
        b = ttk.Button(left, text=name, width=20, command=lambda: set_tool(tool_id))
        b.pack(pady=2)
        return b

    tool_button("Select", "select")
    tool_button("Paint Biome", "paint_biome")
    tool_button("Paint Trail", "paint_trail")
    tool_button("Erase Trail", "erase_trail")
    tool_button("Inspect", "inspect")

    # ---------------------------------------------------------
    # Biome selection panel
    # ---------------------------------------------------------
    ttk.Label(left, text="Biome", font=("Arial", 10, "bold")).pack(pady=6)

    biome_box = ttk.Combobox(left, textvariable=biome_var,
                             values=biome_ids, state="readonly")
    biome_box.pack(pady=4)

    # ---------------------------------------------------------
    # Grid widget (contains layered renderer)
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
    # Connect widget → tools
    # ---------------------------------------------------------

    def handle_click(coord):
        tool = tools[current_tool.get()]
        tool.on_click(coord, grid, grid_widget)

    def handle_drag(event):
        tool = tools[current_tool.get()]
        coord = grid_widget.pixel_to_hex(event.x, event.y)
        if coord in grid.tiles:
            tool.on_drag(coord, grid, grid_widget)

    def handle_release(event):
        tool = tools[current_tool.get()]
        tool.on_release(grid, grid_widget)

    grid_widget.set_on_hex_clicked(handle_click)
    grid_widget.bind("<B1-Motion>", handle_drag)
    grid_widget.bind("<ButtonRelease-1>", handle_release)

    # ---------------------------------------------------------
    # Movement controls
    # ---------------------------------------------------------
    ttk.Label(right, text="Movement").pack(pady=5)

    speed_var = tk.StringVar(value="normal")

    def do_move(idx):
        mode = speed_var.get()
        if engine.move_dir(idx, mode):
            grid_widget.set_party_positions([party.position])
            grid_widget.redraw()
            time_label.config(text=f"Time Tokens: {engine.get_time():.2f}")

    mvf = ttk.Frame(right)
    mvf.pack(pady=10)

    buttons = [
        ("N", 0, 0, 1),
        ("NW", 5, 1, 0),
        ("NE", 1, 1, 2),
        ("SW", 4, 2, 0),
        ("SE", 2, 2, 2),
        ("S", 3, 3, 1),
    ]
    for label, idx, row, col in buttons:
        ttk.Button(mvf, text=label, command=lambda i=idx: do_move(i)).grid(row=row, column=col)

    ttk.Label(right, text="Speed Mode").pack(pady=5)
    ttk.Combobox(right, textvariable=speed_var,
                 values=["cautious", "normal", "fast"], state="readonly").pack(pady=4)

    time_label = ttk.Label(right, text="Time Tokens: 0.00")
    time_label.pack(pady=8)

    # ---------------------------------------------------------
    # File Menu
    # ---------------------------------------------------------
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    filemenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="File", menu=filemenu)

    def save_map():
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        with open(path, "w") as f:
            json.dump(grid.to_dict(), f, indent=2)

        messagebox.showinfo("Saved", "Map saved.")

    def load_map():
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        with open(path) as f:
            data = json.load(f)

        new_grid = HexGrid.from_dict(data)
        new_grid.biome_lib = biome_lib

        engine.grid = new_grid
        grid_widget.grid = new_grid
        grid_widget._compute_canvas_size()
        grid_widget.redraw()

        messagebox.showinfo("Loaded", "Map loaded.")

    filemenu.add_command(label="Save Map", command=save_map)
    filemenu.add_command(label="Load Map", command=load_map)

    root.mainloop()