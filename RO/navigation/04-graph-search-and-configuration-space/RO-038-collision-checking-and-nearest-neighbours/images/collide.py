"""Collision checking and nearest neighbours for this Note (no output when run on its own): the room's bodies and
their boxes, sweep and prune, a bounding-volume hierarchy, clearance, checking a segment, a 3-link arm for
self-collision, distances with headings, a k-d tree that knows headings wrap, and random directions and rotations."""
import numpy as np
from shapely.geometry import LineString, Point, Polygon, box

import cspace as c

R = c.R
WT = 0.12                                       # wall thickness drawn and boxed (m)
W_RAD = 0.25                                    # metres per radian of heading: the rim of the 0.25 m footprint


def furniture():
    """The four pieces of furniture, the cabinet as one body (its two rectangles joined)."""
    T, R1, R2, pink, green = c.furniture()
    return {"table": T, "cabinet": R1.union(R2), "pink pole": pink, "green pole": green}


def walls():
    """The walls as panels about 1 m long, as a mesh stores them: 7 along the bottom, 4 up each side, and 3 on each
    side of the doorway (the last ones shorter where the doorway or a corner cuts them)."""
    t, out = WT, {}
    cuts = lambda a, b: [(x, min(x + 1.0, b)) for x in np.arange(a, b - 1e-9, 1.0)]
    for i, (x0, x1) in enumerate(cuts(0.0, c.W)):
        out[f"bottom wall {i + 1}"] = box(x0, -t, x1, 0)
    for i, (y0, y1) in enumerate(cuts(0.0, c.H)):
        out[f"left wall {i + 1}"] = box(-t, y0, 0, y1)
        out[f"right wall {i + 1}"] = box(c.W, y0, c.W + t, y1)
    for i, (x0, x1) in enumerate(cuts(0.0, c.DOOR[0])):
        out[f"top wall {i + 1}"] = box(x0, c.H, x1, c.H + t)
    for i, (x0, x1) in enumerate(cuts(c.DOOR[1], c.W)):
        out[f"top wall {i + 4}"] = box(x0, c.H, x1, c.H + t)
    return out


def robot(q):
    return Point(q[0], q[1]).buffer(R, quad_segs=64)


def aabb(g):
    return tuple(round(v, 6) for v in g.bounds)          # (xmin, ymin, xmax, ymax)


def overlap(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def collides(q, g):
    """Narrow phase for the disk robot: its centre within 0.25 m of the body."""
    return g.distance(Point(q[0], q[1])) <= R


def sweep_and_prune(boxes):
    """Sort by left edge; each box tests the boxes after it until one starts beyond its right edge.
    Returns the sorted names, the x-overlapping pairs (each with its full box test) and the number of looks."""
    order = sorted(boxes, key=lambda k: boxes[k][0])
    xpairs, looks = [], 0
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            looks += 1
            if boxes[b][0] > boxes[a][2]:
                break
            xpairs.append((a, b, overlap(boxes[a], boxes[b])))
    return order, xpairs, looks


def build_bvh(items, axis=0):
    """Top-down: sort the bodies by their box centre along the axis, split into two equal halves, alternate axes.
    items: list of (name, box). Node: dict(box, axis, kids or name)."""
    bx = (min(b[0] for _, b in items), min(b[1] for _, b in items), max(b[2] for _, b in items),
          max(b[3] for _, b in items))
    if len(items) == 1:
        return dict(box=bx, name=items[0][0])
    items = sorted(items, key=lambda it: it[1][axis] + it[1][axis + 2])
    h = (len(items) + 1) // 2
    return dict(box=bx, axis=axis, kids=[build_bvh(items[:h], 1 - axis), build_bvh(items[h:], 1 - axis)])


def query_bvh(node, qbox, log):
    """Descend from the root: test the node's box; if it overlaps, go into its children; at a leaf report the body."""
    hit = overlap(node["box"], qbox)
    log.append((node, hit))
    if not hit:
        return []
    if "name" in node:
        return [node["name"]]
    return query_bvh(node["kids"][0], qbox, log) + query_bvh(node["kids"][1], qbox, log)


def all_bodies():
    return {**furniture(), **walls()}


def clearance(p):
    """Distance from the robot's body at centre p to the nearest obstacle (m); negative if they overlap."""
    return min(g.distance(Point(*p)) for g in all_bodies().values()) - R


def free(p):
    return clearance(p) > 0


def halving_order(k):
    """Points of a segment split into 2^k equal steps, as fractions t, in halving order: both ends, the middle,
    the quarter points, the eighth points, ... (LaValle 5.3.4)."""
    order = [0.0, 1.0]
    for lev in range(1, k + 1):
        order += [j / 2 ** lev for j in range(1, 2 ** lev, 2)]
    return order


def exact_check(a, b, log, first=True):
    """Hauser's Visible-Exact1: the segment ab is free if d(a, b) <= c(a) + c(b); else check the midpoint and recurse."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if first:
        for p in (a, b):
            log.append((tuple(p), clearance(p)))
            if log[-1][1] <= 0:
                return False
    ca, cb = clearance(a), clearance(b)
    if np.linalg.norm(b - a) <= ca + cb:
        return True
    m = (a + b) / 2
    log.append((tuple(m), clearance(m)))
    if log[-1][1] <= 0:
        return False
    return exact_check(a, m, log, False) and exact_check(m, b, log, False)


# ---- self-collision: a planar arm of three links, each a line segment
LINKS = (1.0, 0.8, 0.6)


def arm(th):
    """Joint positions of the 3-link arm for relative joint angles th (radians), base at (0, 0)."""
    pts, ang, p = [(0.0, 0.0)], 0.0, np.zeros(2)
    for L, t in zip(LINKS, th):
        ang += t
        p = p + L * np.array([np.cos(ang), np.sin(ang)])
        pts.append(tuple(p))
    return pts


def self_collides(th):
    """Links 1 and 3 are the only pair not joined by a joint; they collide if their segments cross."""
    p = arm(th)
    return LineString([p[0], p[1]]).intersects(LineString([p[2], p[3]]))


# ---- distances with headings
def angle_diff(t1, t2):
    """Signed difference t2 - t1 wrapped into (-pi, pi]."""
    d = (t2 - t1 + np.pi) % (2 * np.pi) - np.pi
    return np.pi if d == -np.pi else d


def angle_dist(t1, t2):
    return abs(angle_diff(t1, t2))


def config_dist(q1, q2, w=W_RAD, wrap=True):
    """Distance between (x, theta) or (x, y, theta) configurations: Euclidean on the positions and w times the
    heading difference, wrapped or not."""
    dpos = np.subtract(q1[:-1], q2[:-1])
    dth = angle_dist(q1[-1], q2[-1]) if wrap else abs(q1[-1] - q2[-1])
    return float(np.sqrt(dpos @ dpos + (w * dth) ** 2))


# ---- a k-d tree over (x, theta)
def build_kd(pts, lo=(3.0, 0.0), hi=(4.0, 2 * np.pi), depth=0):
    """Split alternately on x and theta at the median point; leaves hold one point. Each node keeps its cell."""
    axis = depth % 2
    if len(pts) == 1:
        return dict(cell=(lo, hi), pts=pts)
    pts = sorted(pts, key=lambda p: p[axis])
    m = len(pts) // 2
    s = (pts[m - 1][axis] + pts[m][axis]) / 2
    lhi, rlo = list(hi), list(lo)
    lhi[axis], rlo[axis] = s, s
    return dict(cell=(lo, hi), axis=axis, split=s, kids=[build_kd(pts[:m], lo, tuple(lhi), depth + 1),
                                                         build_kd(pts[m:], tuple(rlo), hi, depth + 1)])


def cell_gap(q, cell, wrap):
    """Lower bound on the distance from q to any point of the cell: the gap in x, and the gap in theta measured the
    short way round the circle when wrap is True."""
    (x0, t0), (x1, t1) = cell
    gx = max(x0 - q[0], 0, q[0] - x1)
    if t0 <= q[1] <= t1:
        gt = 0.0
    else:
        gt = min(abs(q[1] - t0), abs(q[1] - t1))
        if wrap:
            gt = min(angle_dist(q[1], t0), angle_dist(q[1], t1))
    return float(np.hypot(gx, W_RAD * gt))


def search_kd(node, q, wrap, best, log):
    """Branch and bound: go first into the child that holds q, then into the other only if its cell may hold a
    nearer point (cell_gap < best distance). log records (cell, "leaf" or "pruned", best so far, the leaf's point or
    None, its distance or the pruned cell's gap)."""
    if "pts" in node:
        p = node["pts"][0]
        d = config_dist(q, p[:2], wrap=wrap)
        if d < best[1]:
            best = (p, d)
        log.append((node["cell"], "leaf", best, p, d))
        return best
    a = node["axis"]
    near, far = (node["kids"] if q[a] < node["split"] else node["kids"][::-1])
    best = search_kd(near, q, wrap, best, log)
    gap = cell_gap(q, far["cell"], wrap)
    if gap < best[1]:
        best = search_kd(far, q, wrap, best, log)
    else:
        log.append((far["cell"], "pruned", best, None, gap))
    return best


# ---- random directions and rotations
def quat_rotate(h, v):
    """Rotate vector v by the unit quaternion h = (a, b, c, d) = a + b i + c j + d k."""
    a, b, cc, d = h
    R_ = np.array([[1 - 2 * (cc * cc + d * d), 2 * (b * cc - a * d), 2 * (b * d + a * cc)],
                   [2 * (b * cc + a * d), 1 - 2 * (b * b + d * d), 2 * (cc * d - a * b)],
                   [2 * (b * d - a * cc), 2 * (cc * d + a * b), 1 - 2 * (b * b + cc * cc)]])
    return R_ @ v


def shoemake(u1, u2, u3):
    """LaValle eq. 5.15: three uniform numbers in [0, 1] give a uniform random unit quaternion."""
    return np.array([np.sqrt(1 - u1) * np.sin(2 * np.pi * u2), np.sqrt(1 - u1) * np.cos(2 * np.pi * u2),
                     np.sqrt(u1) * np.sin(2 * np.pi * u3), np.sqrt(u1) * np.cos(2 * np.pi * u3)])


def sample_directions(n=100_000, seed=0):
    """The samplers of this Note, one seeded stream: 2D directions from a square and from a normal distribution,
    3D points from a uniform latitude angle, from a uniform height (the bread slicer) and from a normal distribution,
    and the up arrow turned by Shoemake's random rotations."""
    rng = np.random.default_rng(seed)
    sq = rng.uniform(-1, 1, (n, 2))
    g2 = rng.normal(size=(n, 2))
    lat, lon = rng.uniform(-np.pi / 2, np.pi / 2, n), rng.uniform(0, 2 * np.pi, n)
    by_lat = np.c_[np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)]
    z, lon2 = rng.uniform(-1, 1, n), rng.uniform(0, 2 * np.pi, n)
    by_height = np.c_[np.sqrt(1 - z ** 2) * np.cos(lon2), np.sqrt(1 - z ** 2) * np.sin(lon2), z]
    g3 = rng.normal(size=(n, 3))
    g3 /= np.linalg.norm(g3, axis=1)[:, None]
    U = rng.uniform(0, 1, (n // 5, 3))
    up = np.array([0.0, 0.0, 1.0])
    rot = np.array([quat_rotate(shoemake(*u), up) for u in U])
    return dict(square=np.degrees(np.arctan2(sq[:, 1], sq[:, 0])) % 360,
                normal2=np.degrees(np.arctan2(g2[:, 1], g2[:, 0])) % 360,
                latitude=by_lat, height=by_height, normal3=g3, rotated=rot)


def near_share(deg, centres, half=5.0):
    """Share of directions within half degrees of any of the given centres (degrees)."""
    d = np.abs((deg[:, None] - np.array(centres)[None, :] + 180) % 360 - 180)
    return float(np.mean(d.min(axis=1) <= half))
