"""Shared numbers and functions for this Note's figures (no output when run on its own).
The room of the beam-model Note: 5 m x 4 m, walls on its four sides, plus a box from x = 3.6 to 4.2 m and
y = 0.6 to 1.2 m. Grid cells are 0.01 m. The robot stands at pose A = (2, 2, 0) and its laser has 12 beams,
one every 30 degrees, z_max = 5 m. A person 1 m ahead blocks the forward beam (reading 1.00 m)."""
import numpy as np
from scipy.ndimage import distance_transform_edt

RES = 0.01                                 # cell size (m)
X0, Y0 = -0.2, -0.2                        # world position of the grid's lower-left corner
NX, NY = 540, 440                         # grid covers x in [-0.2, 5.2), y in [-0.2, 4.2)
ZMAX = 5.0
SIG = 0.1                                  # spread of the endpoint Gaussian (m)
W_HIT, W_RAND = 0.9, 0.1                   # weights of the two parts of the likelihood field
ANGLES = np.radians(np.arange(0, 360, 30))
POSE_A = (2.0, 2.0, 0.0)
BOX = (3.6, 4.2, 0.6, 1.2)


def make_map(box=True):
    """Occupancy grid: True = occupied. Walls are the cells outside the 5 m x 4 m room."""
    xs = X0 + (np.arange(NX) + 0.5) * RES
    ys = Y0 + (np.arange(NY) + 0.5) * RES
    X, Y = np.meshgrid(xs, ys, indexing="xy")              # arrays of shape (NY, NX)
    occ = (X < 0) | (X > 5) | (Y < 0) | (Y > 4)
    if box:
        occ |= (X > BOX[0]) & (X < BOX[1]) & (Y > BOX[2]) & (Y < BOX[3])
    return occ, xs, ys


def cell(x, y):
    return int(np.floor((y - Y0) / RES)), int(np.floor((x - X0) / RES))


def distance_grid(occ):
    """Distance (m) from each cell centre to the nearest occupied cell centre: the Euclidean distance transform."""
    return distance_transform_edt(~occ) * RES


def field(dist, sig=SIG):
    """Likelihood field: density of a beam endpoint in each cell (per m)."""
    g = np.exp(-0.5 * (dist / sig) ** 2) / (sig * np.sqrt(2 * np.pi))
    return W_HIT * g + W_RAND / ZMAX


def raycast(occ, pose, ang, step=0.005):
    x, y, th = pose
    d = 0.0
    while d < ZMAX:
        r, c = cell(x + d * np.cos(th + ang), y + d * np.sin(th + ang))
        if r < 0 or c < 0 or r >= NY or c >= NX or occ[r, c]:
            return d
        d += step
    return ZMAX


def endpoints(pose, z, angles=ANGLES):
    x, y, th = pose
    z = np.asarray(z, float)
    keep = z < ZMAX
    return x + z[keep] * np.cos(th + angles[keep]), y + z[keep] * np.sin(th + angles[keep])


def lookup(grid, px, py):
    """Value of a grid at world points; points outside the grid get the far-away floor value."""
    out = np.full(len(px), W_RAND / ZMAX)
    for i, (a, b) in enumerate(zip(px, py)):
        r, c = cell(a, b)
        if 0 <= r < NY and 0 <= c < NX:
            out[i] = grid[r, c]
    return out


def field_loglik(F, pose, z, angles=ANGLES):
    px, py = endpoints(pose, z, angles)
    return np.log(lookup(F, px, py)).sum()


def scan_A(seed=1):
    """The 12 readings at pose A: true ranges plus small noise; the forward beam reads the person at 1.00 m and
    the four beams of the beam-model Note keep their readings 1.00, 1.97, 2.04, 1.99."""
    occ, _, _ = make_map()
    rng = np.random.default_rng(seed)
    z = np.array([raycast(occ, POSE_A, a) for a in ANGLES])
    z = np.round(z + rng.normal(0, 0.02, len(z)), 2)
    z[0], z[3], z[6], z[9] = 1.00, 1.97, 2.04, 1.99
    return z


# ---- scan matching: two scans of 360 beams, one every degree, no person ----
ANG72 = np.radians(np.arange(0, 360, 1))
POSE_1 = (2.0, 2.0, 0.0)
POSE_2 = (2.3, 2.1, np.radians(5))          # true pose of the second scan; odometry says (2.3, 2.0, 0)
DTH = np.radians(np.arange(-10, 10.5, 1))
DX = np.round(np.arange(-0.1, 0.7001, 0.02), 2)
DY = np.round(np.arange(-0.3, 0.3001, 0.02), 2)


def scan72(pose, seed):
    occ, _, _ = make_map()
    rng = np.random.default_rng(seed)
    z = np.array([raycast(occ, pose, a) for a in ANG72])
    return np.round(z + rng.normal(0, 0.02, len(z)), 2)


def scan_field(z1):
    """Likelihood field built from the endpoints of scan 1 (in scan 1's frame, which is the world frame here)."""
    occ = np.zeros((NY, NX), bool)
    px, py = endpoints((0.0, 0.0, 0.0), z1, ANG72)
    for a, b in zip(px + POSE_1[0], py + POSE_1[1]):
        r, c = cell(a, b)
        if 0 <= r < NY and 0 <= c < NX:
            occ[r, c] = True
    return field(distance_grid(occ))


def match(F1, z2):
    """Score every candidate motion (dx, dy, dth) of scan 2 relative to scan 1: sum of log field values."""
    qx, qy = endpoints((0.0, 0.0, 0.0), z2, ANG72)
    best, scores = None, np.empty((len(DTH), len(DY), len(DX)))
    for i, t in enumerate(DTH):
        rx = np.cos(t) * qx - np.sin(t) * qy
        ry = np.sin(t) * qx + np.cos(t) * qy
        for j, dy in enumerate(DY):
            for k, dx in enumerate(DX):
                scores[i, j, k] = np.log(lookup_fast(F1, rx + POSE_1[0] + dx, ry + POSE_1[1] + dy)).sum()
    i, j, k = np.unravel_index(scores.argmax(), scores.shape)
    return (DX[k], DY[j], np.degrees(DTH[i])), scores


def lookup_fast(grid, px, py):
    r = np.floor((py - Y0) / RES).astype(int)
    c = np.floor((px - X0) / RES).astype(int)
    ok = (r >= 0) & (r < NY) & (c >= 0) & (c < NX)
    out = np.full(len(px), W_RAND / ZMAX)
    out[ok] = grid[r[ok], c[ok]]
    return out


# ---- correlation-based map matching on 0.1 m cells ----
MRES = 0.1
MX = np.arange(0.05, 5.0, MRES)            # cell centres across the room (50 x 40 cells)
MY = np.arange(0.05, 4.0, MRES)


def global_map():
    """1 for cells that touch a surface (the walls' inner faces and the box), 0 for free cells."""
    g = np.zeros((len(MY), len(MX)))
    for j, y in enumerate(MY):
        for i, x in enumerate(MX):
            near_wall = x < MRES or x > 5 - MRES or y < MRES or y > 4 - MRES
            in_box = BOX[0] - MRES < x < BOX[1] + MRES and BOX[2] - MRES < y < BOX[3] + MRES
            inside_box = BOX[0] + MRES < x < BOX[1] - MRES and BOX[2] + MRES < y < BOX[3] - MRES
            g[j, i] = 1.0 if near_wall or (in_box and not inside_box) else 0.0
    return g


def local_map(z2, dx, dy, dth):
    """The scan's endpoints, placed at a candidate pose, marked on the same 0.1 m cells (ends outside are dropped)."""
    qx, qy = endpoints((0.0, 0.0, 0.0), z2, ANG72)
    px = np.cos(dth) * qx - np.sin(dth) * qy + POSE_1[0] + dx
    py = np.sin(dth) * qx + np.cos(dth) * qy + POSE_1[1] + dy
    l = np.zeros((len(MY), len(MX)))
    i = np.clip(np.floor(px / MRES).astype(int), 0, len(MX) - 1)
    j = np.clip(np.floor(py / MRES).astype(int), 0, len(MY) - 1)
    l[j, i] = 1.0
    return l


def corr(g, l):
    """Pearson correlation of two maps, cell by cell."""
    a, b = g.ravel() - g.mean(), l.ravel() - l.mean()
    return (a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum())
