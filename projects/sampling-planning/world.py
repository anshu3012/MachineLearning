"""Worlds are plain files in worlds/. `load_world` turns one into a Space the planners can run in.

worlds/<name>.json holds, in metres:
  name, about   what the world is
  bounds        [x0, y0, x1, y1], the outer walls
  obstacles     a list; each is a rectangle [x0, y0, x1, y1] or a polygon [[x, y], [x, y], ...]
  start, goal   [x, y]
  robot_radius  the robot is a disk of this radius
  step          (optional) how far a tree grows per sample; default: 1/25 of the bounds' diagonal
  eps           (optional) edge resolution; default: robot_radius / 5
  notes         (optional) [[x, y, "label"], ...] written on the map
A grid map from the grid project (a PNG in projects/grid-pathfinding/maps/, read by that project's own loader) is
turned into such a file first. Every load redraws worlds/<name>.png when it is missing or older than its json."""
import json
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from collision import Space

WORLDS = Path(__file__).resolve().parent / "worlds"
GRID_PROJECT = Path(__file__).resolve().parents[1] / "grid-pathfinding"


def load_world(arg):
    """arg: a world name in worlds/ ("office"), a path to a world .json, or a path to a grid map .png."""
    path = Path(arg)
    if path.suffix == ".png":  # a grid map: write it as a world file first (only if it changed)
        text = json.dumps(grid_to_world(path), indent=1)
        path = WORLDS / f"{path.stem}.json"
        if not path.exists() or path.read_text() != text:
            path.write_text(text)
    elif path.suffix != ".json":
        path = WORLDS / f"{arg}.json"
    world = json.loads(path.read_text())
    shapes = [box(*o) if isinstance(o[0], (int, float)) else Polygon(o) for o in world["obstacles"]]
    world["free_region"] = box(*world["bounds"]).difference(unary_union(shapes))
    space = Space(world)
    space.key = path.stem
    picture = path.with_suffix(".png")
    if not picture.exists() or picture.stat().st_mtime < path.stat().st_mtime:
        import render  # only drawing needs Plotly
        render.world_picture(space, picture)
    return space


def grid_to_world(png, radius=None):
    """A grid map image -> a world dict, in the grid project's own coordinates (cell centres at whole multiples of
    the cell size). Each run of blocked cells along a row becomes one rectangle. The robot radius defaults to a
    quarter cell, so the robot fits through a one-cell gap; the tree step is one cell."""
    sys.path.append(str(GRID_PROJECT))
    from grid import load_grid  # the grid project's reader: same colours, same cell size file, same coordinates
    g = load_grid(png)
    rows, cols = g.free.shape
    h = g.cell / 2
    rects = []
    for r in range(rows):
        c = 0
        while c < cols:
            if g.free[r, c]:
                c += 1
                continue
            first = c
            while c < cols and not g.free[r, c]:
                c += 1
            (xa, y), (xb, _) = g.xy((first, r)), g.xy((c - 1, r))
            rects.append([xa - h, y - h, xb + h, y + h])
    (x0, y1), (x1, y0) = g.xy((0, 0)), g.xy((cols - 1, rows - 1))
    return dict(name=g.label, about=f"Grid map {Path(png).name} from the grid project: {cols} x {rows} cells of "
                f"{g.cell:g} m.", bounds=[x0 - h, y0 - h, x1 + h, y1 + h], robot_radius=g.cell / 4 if radius is None
                else radius, step=g.cell, start=list(g.xy(g.start)), goal=list(g.xy(g.goal)), obstacles=rects)


def street_world(roads, road_width, start, goal, robot_radius):
    """Hook for a street map, for the real-map project to fill in. The free region is the road network: the road
    centre lines (shapely LineStrings, in metres) buffered by half the road width. Build a world dict with the keys
    above plus "free_region", then Space(world); the planners and the drawing code need nothing else."""
    raise NotImplementedError("street worlds are built by projects/real-map-pathfinding")
