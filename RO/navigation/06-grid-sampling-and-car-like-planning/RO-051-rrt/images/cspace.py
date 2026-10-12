"""Shared geometry for this Note (no output when run on its own): the room of RO-009 (roommap.py), the robot's
disk footprint of radius 0.25 m, a 1.4 m x 0.3 m board carried along the heading, and their obstacles in C-space.
Walls are solid slabs outside the room; the doorway (x = 3.0 to 4.2 m in the top wall) is open."""
import numpy as np
import shapely
from shapely.geometry import MultiPoint, Point, Polygon, box
from shapely.ops import unary_union

from roommap import CAB, DOOR, H, POLE_R, POLES, TABLE, W

R = 0.25                                     # disk footprint radius (m), centred on the middle of the axle
BOARD = (1.4, 0.3)                           # board length along the heading and width (m)
START = (2.0, 1.0, np.radians(30))           # the robot's pose (x, y, heading)
GOAL = (3.6, 4.0)                            # the doorway centre
TEST = (3.5, 3.2)                            # 0.2 m straight above the table's top-left corner (3.5, 3.0)
BIG = 3.0                                    # wall slab thickness used in the computations (m)


def circle(cx, cy, r, n=96):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return Polygon(np.c_[cx + r * np.cos(t), cy + r * np.sin(t)])


def walls():
    """Five slabs: bottom, left, right, and the top wall left and right of the doorway."""
    b = BIG
    return [box(-b, -b, W + b, 0), box(-b, -b, 0, H + b), box(W, -b, W + b, H + b),
            box(-b, H, DOOR[0], H + b), box(DOOR[1], H, W + b, H + b)]


def furniture():
    """Convex pieces: the table, the cabinet's two rectangles, the two poles."""
    return ([Polygon(TABLE)] + [box(x0, y0, x1, y1) for x0, x1, y0, y1 in CAB]
            + [circle(px, py, POLE_R) for px, py in POLES.values()])


def pieces():
    return furniture() + walls()


def obstacles():
    return unary_union(pieces())


def cobs_disk(r=R):
    """C-obstacle of the disk robot: every obstacle grown by r (all points within r of an obstacle)."""
    return unary_union([p.buffer(r, quad_segs=64) for p in pieces()])


def board(th, L=BOARD[0], w=BOARD[1]):
    """Corners of the board centred on (0, 0) and turned to heading th (counter-clockwise order)."""
    c, s = np.cos(th), np.sin(th)
    pts = [(L / 2, -w / 2), (L / 2, w / 2), (-L / 2, w / 2), (-L / 2, -w / 2)]
    return [(c * x - s * y, s * x + c * y) for x, y in pts]


def msum(P, Q):
    """Minkowski sum of two convex polygons given by corner lists: the convex hull of all corner sums."""
    return MultiPoint([(a[0] + b[0], a[1] + b[1]) for a in P for b in Q]).convex_hull


def corners(poly):
    return list(poly.exterior.coords)[:-1]


def cobs_board_piece(piece, th):
    neg = [(-x, -y) for x, y in board(th)]          # the board reflected through its centre
    return msum(corners(piece), neg)


def cobs_board(th):
    """C-obstacle slice of the board robot at heading th: every convex piece summed with the reflected board."""
    return unary_union([cobs_board_piece(p, th) for p in pieces()])


def free_grid(cobs, h=0.01, ymax=H):
    """Boolean grid of free centres over the room box [0, W] x [0, ymax], spacing h; returns xs, ys, mask."""
    xs = np.arange(0, W + 1e-9, h)
    ys = np.arange(0, ymax + 1e-9, h)
    X, Y = np.meshgrid(xs, ys)
    shapely.prepare(cobs)
    return xs, ys, ~shapely.intersects_xy(cobs, X, Y)


def door_gap(cobs, n=12001):
    """Width of the free stretch of the doorway line y = 4 for the robot's centre."""
    xs = np.linspace(DOOR[0], DOOR[1], n)
    shapely.prepare(cobs)
    free = xs[~shapely.intersects_xy(cobs, xs, np.full(n, H))]
    return float(free.max() - free.min()) if free.size else 0.0


def turns(poly):
    """Turning angle at each corner of a counter-clockwise convex polygon, in degrees."""
    P = np.array(corners(poly))
    out = []
    for i in range(len(P)):
        d1, d2 = P[i] - P[i - 1], P[(i + 1) % len(P)] - P[i]
        out.append(np.degrees(np.arctan2(d1[0] * d2[1] - d1[1] * d2[0], d1 @ d2)))
    return out


def outline(geom):
    """x and y lists tracing every ring of a (multi)polygon, rings separated by None (for Plotly)."""
    xs, ys = [], []
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        for ring in [g.exterior] + list(g.interiors):
            x, y = ring.xy
            xs += list(x) + [None]
            ys += list(y) + [None]
    return xs, ys
