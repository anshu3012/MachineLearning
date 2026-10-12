"""The cup holder at B and the motion "move down" with an error (no output when run on its own).

The holder is two posts on the table, 1.5 cm thick and 2 cm tall, with a 45-degree chamfer 1 cm wide on each inner
top corner; the gap between them is 7 cm at the bottom, so the 6 cm cup has 0.5 cm of play on each side. In the cup's
C-space (the position of the middle of the cup's bottom, RO-037's Minkowski sum with the cup reflected), the cup is a
point and the gap is a slot 1 cm wide. The command "move down" moves the point in a straight line whose direction
may be off by up to 10 degrees from straight down; on touching a surface it slides along it if the push along the
surface beats friction (friction coefficient 0.4: the motion must point more than 21.8 degrees away from straight
into the surface), and otherwise it sticks (LaValle 12.5.1, compliant motions). The goal: resting in the slot."""
import numpy as np
import shapely
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box

import manip as m

B, TOP = m.B_X, m.TOP
POST_T, POST_H, CHAMFER = 0.015, 0.02, 0.01
GAP = 0.07                                       # inner gap at the bottom (m)
ERR = 10.0                                       # direction error of a motion command (degrees)
MU = 0.4
FRICTION_ANGLE = np.degrees(np.arctan(MU))       # 21.8 degrees
GOAL_HALF = (GAP - m.CUP_W) / 2                  # 0.005 m of play on each side
MOUTH = TOP + POST_H                             # height of the posts' tops


def posts():
    """The two posts in the room, as polygons (side view)."""
    a = B - GAP / 2
    left = Polygon([(a - POST_T, TOP), (a, TOP), (a, TOP + POST_H - CHAMFER), (a - CHAMFER, TOP + POST_H),
                    (a - POST_T, TOP + POST_H)])
    right = Polygon([(2 * B - x, y) for x, y in left.exterior.coords][::-1])
    return left, right


def cobs_piece(poly):
    """C-obstacle of a convex piece for the cup's bottom-centre point: the piece plus the cup reflected."""
    cup = [(-m.CUP_W / 2, 0), (m.CUP_W / 2, 0), (m.CUP_W / 2, -m.CUP_H), (-m.CUP_W / 2, -m.CUP_H)]
    return MultiPoint([(x + a, y + b) for x, y in poly.exterior.coords for a, b in cup]).convex_hull


def cobs():
    pieces = [cobs_piece(p) for p in posts()] + [cobs_piece(m.bottle()), box(-1, -1, 1, TOP)]
    return shapely.union_all(pieces)


O = cobs()
EDGES = []
for ring in [O.exterior] + list(O.interiors):
    c = list(ring.coords)
    EDGES += [(np.array(c[i]), np.array(c[i + 1])) for i in range(len(c) - 1)]


def normal(a, b):
    """Unit normal of edge ab pointing out of the obstacle (into free space)."""
    t = (b - a) / np.linalg.norm(b - a)
    n = np.array([-t[1], t[0]])
    mid = (a + b) / 2 + 1e-6 * n
    return n if not O.contains(Point(mid)) else -n


NORMALS = [normal(a, b) for a, b in EDGES]


def inside(q):
    """Strictly inside the obstacles: further than 1e-9 m from their boundary (guards against rounding)."""
    return O.contains(Point(q)) and O.boundary.distance(Point(q)) > 1e-9


def in_goal(p):
    return abs(p[1] - TOP) < 1e-7 and abs(p[0] - B) <= GOAL_HALF + 1e-9


def ray_hit(p, d):
    """First edge hit by the ray from p along d: (distance, edge index); None if nothing within 1 m."""
    best = None
    for i, (a, b) in enumerate(EDGES):
        e = b - a
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = a - p
        t = (w[0] * e[1] - w[1] * e[0]) / den
        s = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-10 and -1e-12 <= s <= 1 + 1e-12 and np.dot(d, NORMALS[i]) < 0:
            if best is None or t < best[0] - 1e-12:
                best = (t, i)
    return best


def incident(p):
    """Edges that p lies on (it may be a corner shared by two edges)."""
    out = []
    for i, (a, b) in enumerate(EDGES):
        e = b - a
        t = np.clip(np.dot(p - a, e) / np.dot(e, e), 0, 1)
        if np.linalg.norm(a + t * e - p) < 1e-9:
            out.append(i)
    return out


def slides_away(i, p, d):
    """True if sliding along edge i from p, in the direction of the motion d, moves along the edge (not off it)."""
    a, b = EDGES[i]
    t = b - a
    if np.dot(t, d) < 0:
        t = -t
    end = b if np.dot(b - a, t) > 0 else a
    return np.linalg.norm(end - p) > 1e-9


def run(p, angle_deg, slide=True, log=None, max_steps=20):
    """Move from p in direction angle_deg (270 = straight down) until stuck. Returns (end point, reached goal)."""
    p = np.array(p, float)
    d = np.array([np.cos(np.radians(angle_deg)), np.sin(np.radians(angle_deg))])
    if log is not None:
        log.append(p.copy())
    for _ in range(max_steps):
        touching = [i for i in incident(p) if np.dot(d, NORMALS[i]) < -1e-12 and slides_away(i, p, d)]
        if touching:
            i = min(touching, key=lambda j: np.dot(d, NORMALS[j]))
        elif inside(p + 1e-7 * d):
            return p, in_goal(p)                                          # pushed into a corner: stuck
        else:
            hit = ray_hit(p, d)
            if hit is None:
                return p, False
            p = p + hit[0] * d
            i = hit[1]
            if log is not None:
                log.append(p.copy())
            if not inside(p + 1e-7 * d):
                continue                                                  # grazed a corner: keep moving
        n = NORMALS[i]
        into = np.degrees(np.arccos(np.clip(np.dot(d, -n), -1, 1)))       # angle from straight into the surface
        if not slide or into <= FRICTION_ANGLE:
            return p, in_goal(p)
        a, b = EDGES[i]
        t = (b - a) / np.linalg.norm(b - a)
        if np.dot(t, d) < 0:
            t = -t
        if inside(p + 1e-6 * t + 1e-7 * n) or not slides_away(i, p, d):
            return p, in_goal(p)                                          # a corner stops the sliding
        p = (b if np.dot(b - a, t) > 0 else a).copy()                   # slide to the end of the edge
        if log is not None:
            log.append(p.copy())
    return p, in_goal(p)


ANGLES = np.linspace(270 - ERR, 270 + ERR, 21)


def guaranteed(p, slide=True):
    """True if every direction within the error reaches the goal: p is in the preimage of the goal."""
    if O.contains(Point(p)) or O.boundary.distance(Point(p)) < 1e-9 and not in_goal(p):
        return False
    return all(run(p, a, slide)[1] for a in ANGLES)


def preimage_grid(slide, h=0.001, x0=B - 0.05, x1=B + 0.05, y1=MOUTH + 0.11):
    xs = np.arange(x0, x1 + 1e-9, h)
    ys = np.arange(TOP + h, y1 + 1e-9, h)
    G = np.array([[guaranteed((x, y), slide) for x in xs] for y in ys])
    return xs, ys, G
