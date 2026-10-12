"""Grid maps: a floor plan drawn as a picture, turned into a graph of free cells.

The map file is a PNG in maps/: black = blocked (shelf or wall), white = free floor, pure green = start, pure red =
goal, pure blue = the goals of the multi-goal search. A JSON file with the same name says how big a cell is:
{"label": "Warehouse floor", "cell_m": 1.0, "pixels_per_cell": 1}."""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

from map_interface import Map

MAPS = Path(__file__).resolve().parent / "maps"


class Grid(Map):
    """A grid of square cells. A node is a free cell (col, row), row 0 at the top. A robot moves to any of the 8
    cells around it; a diagonal move needs both cells beside it free, so it never cuts a shelf's corner."""
    MOVES = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]   # N E S W, then diagonals

    def __init__(self, free, cell=1.0, start=None, goal=None, goals=(), name="", label="", origin=(0.0, 0.0)):
        self.free = free                   # 2D bool array: free[row, col] is True on the floor
        self.cell = cell                   # side of a cell in metres
        self.start, self.goal, self.goals = start, goal, tuple(goals)
        self.name, self.label = name, label
        self.origin = origin               # (x, y) in metres of the centre of the bottom-left cell

    def passable(self, c, r):
        return 0 <= r < self.free.shape[0] and 0 <= c < self.free.shape[1] and bool(self.free[r, c])

    def nodes(self):
        rows, cols = np.nonzero(self.free)
        return [(int(c), int(r)) for r, c in zip(rows, cols)]

    def neighbours(self, node):
        c, r = node
        out = []
        for dc, dr in self.MOVES:
            if not self.passable(c + dc, r + dr):
                continue
            if dc and dr and not (self.passable(c + dc, r) and self.passable(c, r + dr)):
                continue                   # a diagonal move would cut a corner
            out.append((c + dc, r + dr))
        return out

    def cost(self, a, b):
        return self.cell * math.hypot(b[0] - a[0], b[1] - a[1])

    def xy(self, node):
        c, r = node
        return (self.origin[0] + c * self.cell, self.origin[1] + (self.free.shape[0] - 1 - r) * self.cell)

    def line_of_sight(self, a, b):
        """True if the straight line between the centres of cells a and b passes only through free cells (and never
        squeezes between two blocked cells that touch at a corner). Walks the cells the line crosses, in order."""
        (c, r), (c1, r1) = a, b
        dc, dr = abs(c1 - c), abs(r1 - r)
        sc, sr = (c1 > c) - (c1 < c), (r1 > r) - (r1 < r)
        i = j = 0                          # cell borders crossed so far, sideways and up/down
        while (c, r) != (c1, r1):
            # the line meets its next sideways border at t = (2i+1)/(2 dc), its next up/down border at
            # t = (2j+1)/(2 dr); compare them as whole numbers so that a corner is found exactly
            tx, ty = (2 * i + 1) * dr, (2 * j + 1) * dc
            if dc and (not dr or tx < ty):
                c, i = c + sc, i + 1
            elif dr and (not dc or ty < tx):
                r, j = r + sr, j + 1
            else:                          # the line passes exactly through a corner
                if not (self.passable(c + sc, r) and self.passable(c, r + sr)):
                    return False
                c, r, i, j = c + sc, r + sr, i + 1, j + 1
            if not self.passable(c, r):
                return False
        return True


def load_grid(name_or_path):
    """Read maps/<name>.png (or any PNG path) and its JSON beside it into a Grid."""
    path = Path(name_or_path)
    if path.suffix != ".png":
        path = MAPS / f"{name_or_path}.png"
    meta_path = path.with_suffix(".json")
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    img = Image.open(path).convert("RGB")
    k = meta.get("pixels_per_cell", 1)
    if k > 1:                              # one cell is drawn as a k x k block of pixels: keep one pixel per block
        img = img.resize((img.width // k, img.height // k), Image.NEAREST)
    px = np.asarray(img).astype(int)
    red, green, blue = px[..., 0], px[..., 1], px[..., 2]
    is_start = (green > 200) & (red < 100) & (blue < 100)
    is_goal = (red > 200) & (green < 100) & (blue < 100)
    is_goals = (blue > 200) & (red < 100) & (green < 100)
    free = (px.mean(axis=2) >= 128) | is_start | is_goal | is_goals
    cells = lambda mask: [(int(c), int(r)) for r, c in zip(*np.nonzero(mask))]
    assert len(cells(is_start)) == 1 and len(cells(is_goal)) == 1, f"{path.name}: draw one green and one red pixel"
    return Grid(free, cell=meta.get("cell_m", 1.0), start=cells(is_start)[0], goal=cells(is_goal)[0],
                goals=cells(is_goals), name=path.stem, label=meta.get("label", path.stem))
