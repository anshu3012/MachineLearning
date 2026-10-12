"""The room of this Note (no output when run on its own): 7 m x 4 m, a door in the top wall from x = 3.0 to 4.2 m,
a table (convex polygon, four half-planes), an L-shaped cabinet (union of two rectangles) and two poles used as
landmarks. Also: the inside test, a bitmap of the room, and a simulated laser scan with pole extraction."""
import numpy as np

W, H = 7.0, 4.0
DOOR = (3.0, 4.2)
TABLE = [(3.0, 1.0), (5.0, 1.0), (5.5, 2.5), (3.5, 3.0)]          # counter-clockwise corners
# Edge functions f(x, y) = a x + b y + c, scaled to whole numbers; f <= 0 on the inside (left of each edge)
TABLE_F = [(0, -1, 1), (3, -1, -14), (2, 8, -31), (-4, 1, 11)]
CAB = [(5.6, 7.0, 3.4, 4.0), (6.4, 7.0, 2.4, 4.0)]                 # two rectangles (x0, x1, y0, y1)
POLES = {"pink": (1.0, 3.0), "green": (6.0, 0.8)}                  # landmark centres, signature = colour
POLE_R = 0.1
ROBOT = (2.0, 1.0, np.radians(30))


def f_table(x, y):
    return [a * x + b * y + c for a, b, c in TABLE_F]


def in_table(x, y):
    return all(v <= 0 for v in f_table(x, y))


def in_rect(x, y, r):
    return r[0] <= x <= r[1] and r[2] <= y <= r[3]


def in_cabinet(x, y):
    return in_rect(x, y, CAB[0]) or in_rect(x, y, CAB[1])


def occupied(x, y):
    """Obstacle test for a point: table, cabinet or pole (walls are the room's border)."""
    if in_table(x, y) or in_cabinet(x, y):
        return True
    return any(np.hypot(x - px, y - py) <= POLE_R for px, py in POLES.values())


def bitmap(cell, sub=10):
    """1 for every cell that contains at least one obstacle point (checked on a sub x sub grid of points)."""
    nx, ny = int(round(W / cell)), int(round(H / cell))
    B = np.zeros((ny, nx), dtype=int)
    t = (np.arange(sub + 1) / sub) * cell
    for j in range(ny):
        for i in range(nx):
            B[j, i] = any(occupied(i * cell + a, j * cell + b) for a in t for b in t)
    return B


def _seg_hit(px, py, dx, dy, ax, ay, bx, by):
    ex, ey = bx - ax, by - ay
    den = dx * ey - dy * ex
    if abs(den) < 1e-12:
        return np.inf
    t = ((ax - px) * ey - (ay - py) * ex) / den
    s = ((ax - px) * dy - (ay - py) * dx) / den
    return t if t > 1e-9 and 0 <= s <= 1 else np.inf


def _segments():
    segs = [(0, 0, W, 0), (W, 0, W, H), (0, H, 0, 0), (0, H, DOOR[0], H), (DOOR[1], H, W, H)]
    segs += [(*TABLE[i], *TABLE[(i + 1) % 4]) for i in range(4)]
    for x0, x1, y0, y1 in CAB:
        segs += [(x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)]
    return segs


def scan(pose, n=360, max_range=8.0, noise=0.0, rng=None):
    """Laser scan: n beams over a full turn, bearing measured from the robot's heading (positive = left)."""
    x, y, th = pose
    bearings = np.radians(np.arange(n) * 360 / n - 180)
    ranges = []
    for b in bearings:
        dx, dy = np.cos(th + b), np.sin(th + b)
        r = min(_seg_hit(x, y, dx, dy, *s) for s in _segments())
        for px, py in POLES.values():                         # circle hit
            fx, fy = x - px, y - py
            bq = fx * dx + fy * dy
            c = fx * fx + fy * fy - POLE_R ** 2
            disc = bq * bq - c
            if disc >= 0:
                t = -bq - np.sqrt(disc)
                if t > 0:
                    r = min(r, t)
        ranges.append(min(r, max_range))
    ranges = np.array(ranges)
    if noise:
        ranges = ranges + rng.normal(0, noise, n)
    return bearings, ranges


def extract_poles(bearings, ranges, jump=0.3, max_width=0.35):
    """Split the scan where the range jumps by more than `jump`; a short segment nearer than both neighbours is a
    pole. Returns (range to centre, bearing) for each: mean bearing, nearest range plus the pole radius."""
    n = len(ranges)
    cuts = [i for i in range(n) if abs(ranges[i] - ranges[i - 1]) > jump]
    found = []
    for k, start in enumerate(cuts):
        end = cuts[(k + 1) % len(cuts)]
        idx = [(start + j) % n for j in range((end - start) % n)]
        if not idx:
            continue
        r = ranges[idx]
        width = r.mean() * abs(bearings[1] - bearings[0]) * len(idx)
        before, after = ranges[(start - 1) % n], ranges[end % n]
        if width <= max_width and r.mean() < before - jump and r.mean() < after - jump:
            b = np.arctan2(np.sin(bearings[idx]).mean(), np.cos(bearings[idx]).mean())
            found.append((r.min() + POLE_R, b, len(idx)))
    return found
