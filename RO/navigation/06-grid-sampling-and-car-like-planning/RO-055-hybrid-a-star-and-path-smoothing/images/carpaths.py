"""Shortest paths for a vehicle that drives at one speed and cannot turn tighter than a radius rho (no output when run
on its own; run with any argument for the self-check).

Dubins paths (forward only, MR 13.3.3; Dubins 1957): the six words LSL, RSR, LSR, RSL, LRL, RLR, built from the
circles of radius rho that touch the start and the goal pose (the tangent-circle construction of Becker's video and
Giese's tutorial). Reeds-Shepp paths (forward and reverse, Reeds and Shepp 1990): the formula families CSC, CCC, CCCC,
CCSC and CCSCC with their time-flip and reflection variants, in the form used by OMPL's ReedsSheppStateSpace.

A path is a list of segments (kind, length) with kind in 'L', 'S', 'R' and length in metres, negative when driven in
reverse. sample() turns it into poses; every word is checked by driving it and comparing the end with the goal."""
import math

import numpy as np

TWO_PI = 2 * math.pi


def mod2pi(a):
    """Angle in [0, 2 pi)."""
    return a % TWO_PI


def wrap(a):
    """Angle in (-pi, pi]."""
    return math.atan2(math.sin(a), math.cos(a))


def step(pose, kind, length, rho):
    """End pose after one segment: arc of radius rho to the left (L) or right (R), or a straight line (S)."""
    x, y, th = pose
    if kind == "S":
        return (x + length * math.cos(th), y + length * math.sin(th), th)
    turn = length / rho if kind == "L" else -length / rho
    if kind == "L":
        x += rho * (math.sin(th + turn) - math.sin(th))
        y -= rho * (math.cos(th + turn) - math.cos(th))
    else:
        x -= rho * (math.sin(th + turn) - math.sin(th))
        y += rho * (math.cos(th + turn) - math.cos(th))
    return (x, y, th + turn)


def endpoint(start, path, rho):
    p = start
    for kind, length in path:
        p = step(p, kind, length, rho)
    return p


def length(path):
    return sum(abs(s) for _, s in path)


def sample(start, path, rho, ds=0.02):
    """Poses every ds metres along the path (and at every segment end); returns an (n, 3) array."""
    out = [start]
    p = start
    for kind, s in path:
        n = max(1, int(math.ceil(abs(s) / ds)))
        for k in range(1, n + 1):
            out.append(step(p, kind, s * k / n, rho))
        p = out[-1]
    return np.array(out)


def _close(a, b, tol=1e-6):
    return math.hypot(a[0] - b[0], a[1] - b[1]) < tol and abs(wrap(a[2] - b[2])) < 1e-6


# ---------------------------------------------------------------- Dubins: tangent circles
def circles(pose, rho):
    """Centres of the left and right turning circles that touch the pose."""
    x, y, th = pose
    return {"L": (x - rho * math.sin(th), y + rho * math.cos(th)),
            "R": (x + rho * math.sin(th), y - rho * math.cos(th))}


def dubins_words(start, goal, rho):
    """All valid Dubins words from start to goal: dict word -> path (list of (kind, length))."""
    c0, c1 = circles(start, rho), circles(goal, rho)
    th0, th1 = start[2], goal[2]
    out = {}
    for a, b in (("L", "L"), ("R", "R"), ("L", "R"), ("R", "L")):
        dx, dy = c1[b][0] - c0[a][0], c1[b][1] - c0[a][1]
        d = math.hypot(dx, dy)
        phi = math.atan2(dy, dx)
        if a == b:
            ths, ls = phi, d                                  # outer tangent: parallel to the centre line
        else:
            if d < 2 * rho:
                continue                                      # the circles overlap: no inner tangent
            ls = math.sqrt(d * d - 4 * rho * rho)
            ths = phi + math.atan2(2 * rho, ls) if a == "L" else phi - math.atan2(2 * rho, ls)
        t1 = mod2pi(ths - th0) if a == "L" else mod2pi(th0 - ths)
        t3 = mod2pi(th1 - ths) if b == "L" else mod2pi(ths - th1)
        out[a + "S" + b] = [(a, rho * t1), ("S", ls), (b, rho * t3)]
    for a, m in (("L", "R"), ("R", "L")):
        dx, dy = c1[a][0] - c0[a][0], c1[a][1] - c0[a][1]
        d = math.hypot(dx, dy)
        if d > 4 * rho or d < 1e-12:
            continue
        phi, gam = math.atan2(dy, dx), math.acos(d / (4 * rho))
        best = None
        for sgn in (1, -1):
            psi = phi + sgn * gam
            cm = (c0[a][0] + 2 * rho * math.cos(psi), c0[a][1] + 2 * rho * math.sin(psi))
            psi2 = math.atan2(cm[1] - c1[a][1], cm[0] - c1[a][0])
            if a == "L":                                      # car on a left circle: heading = radius angle + 90 deg
                h1, h2 = psi + math.pi / 2, psi2 + math.pi / 2
                t1, t2, t3 = mod2pi(h1 - th0), mod2pi(h1 - h2), mod2pi(th1 - h2)
            else:
                h1, h2 = psi - math.pi / 2, psi2 - math.pi / 2
                t1, t2, t3 = mod2pi(th0 - h1), mod2pi(h2 - h1), mod2pi(h2 - th1)
            p = [(a, rho * t1), (m, rho * t2), (a, rho * t3)]
            if best is None or length(p) < length(best):
                best = p
        out[a + m + a] = best
    for w, p in out.items():
        assert _close(endpoint(start, p, rho), goal), w
    return out


def dubins(start, goal, rho):
    """(word, path) of the shortest Dubins path."""
    words = dubins_words(start, goal, rho)
    w = min(words, key=lambda k: length(words[k]))
    return w, words[w]


# ---------------------------------------------------------------- Reeds-Shepp: formula families
ZERO = 1e-9
HALF_PI = math.pi / 2
TYPES = ["LRL", "RLR", "LRLR", "RLRL", "LRSL", "RLSR", "LSRL", "RSLR", "LRSR", "RLSL", "RSRL", "LSLR",
         "LSR", "RSL", "LSL", "RSR", "LRSLR", "RLSRL"]


def _m2p(x):
    """Angle in (-pi, pi], as in the Reeds-Shepp formulas."""
    v = math.fmod(x, TWO_PI)
    if v < -math.pi:
        v += TWO_PI
    elif v > math.pi:
        v -= TWO_PI
    return v


def _polar(x, y):
    return math.hypot(x, y), math.atan2(y, x)


def _tau_omega(u, v, xi, eta, phi):
    delta = _m2p(u - v)
    a = math.sin(u) - math.sin(delta)
    b = math.cos(u) - math.cos(delta) - 1
    t1 = math.atan2(eta * a - xi * b, xi * a + eta * b)
    t2 = 2 * (math.cos(delta) - math.cos(v) - math.cos(u)) + 3
    tau = _m2p(t1 + math.pi) if t2 < 0 else _m2p(t1)
    return tau, _m2p(tau - u + v - phi)


def _lpslp(x, y, phi):
    u, t = _polar(x - math.sin(phi), y - 1 + math.cos(phi))
    if t >= -ZERO:
        v = _m2p(phi - t)
        if v >= -ZERO:
            return t, u, v
    return None


def _lpsrp(x, y, phi):
    u1, t1 = _polar(x + math.sin(phi), y - 1 - math.cos(phi))
    u1 = u1 * u1
    if u1 >= 4:
        u = math.sqrt(u1 - 4)
        t = _m2p(t1 + math.atan2(2, u))
        v = _m2p(t - phi)
        if t >= -ZERO and v >= -ZERO:
            return t, u, v
    return None


def _lprml(x, y, phi):
    u1, theta = _polar(x - math.sin(phi), y - 1 + math.cos(phi))
    if u1 <= 4:
        u = -2 * math.asin(0.25 * u1)
        t = _m2p(theta + 0.5 * u + math.pi)
        v = _m2p(phi - t + u)
        if t >= -ZERO and u <= ZERO:
            return t, u, v
    return None


def _lprupumrm(x, y, phi):
    xi, eta = x + math.sin(phi), y - 1 - math.cos(phi)
    rho = 0.25 * (2 + math.hypot(xi, eta))
    if rho <= 1:
        u = math.acos(rho)
        t, v = _tau_omega(u, -u, xi, eta, phi)
        if t >= -ZERO and v <= ZERO:
            return t, u, v
    return None


def _lprumlumrp(x, y, phi):
    xi, eta = x + math.sin(phi), y - 1 - math.cos(phi)
    rho = (20 - xi * xi - eta * eta) / 16
    if 0 <= rho <= 1:
        u = -math.acos(rho)
        if u >= -HALF_PI:
            t, v = _tau_omega(u, u, xi, eta, phi)
            if t >= -ZERO and v >= -ZERO:
                return t, u, v
    return None


def _lprmsmlm(x, y, phi):
    rho, theta = _polar(x - math.sin(phi), y - 1 + math.cos(phi))
    if rho >= 2:
        r = math.sqrt(rho * rho - 4)
        u = 2 - r
        t = _m2p(theta + math.atan2(r, -2))
        v = _m2p(phi - HALF_PI - t)
        if t >= -ZERO and u <= ZERO and v <= ZERO:
            return t, u, v
    return None


def _lprmsmrm(x, y, phi):
    xi, eta = x + math.sin(phi), y - 1 - math.cos(phi)
    rho, theta = _polar(-eta, xi)
    if rho >= 2:
        t = theta
        u = 2 - rho
        v = _m2p(t + HALF_PI - phi)
        if t >= -ZERO and u <= ZERO and v <= ZERO:
            return t, u, v
    return None


def _lprmslmrp(x, y, phi):
    xi, eta = x + math.sin(phi), y - 1 - math.cos(phi)
    rho, _ = _polar(xi, eta)
    if rho >= 2:
        u = 4 - math.sqrt(rho * rho - 4)
        if u <= ZERO:
            t = _m2p(math.atan2((4 - u) * xi - 2 * eta, -2 * xi + (u - 4) * eta))
            v = _m2p(t - phi)
            if t >= -ZERO and v >= -ZERO:
                return t, u, v
    return None


def _candidates(x, y, phi):
    """Every Reeds-Shepp candidate for a goal (x, y, phi) seen from the start, in units of rho: (type, lengths)."""
    out = []
    xb, yb = x * math.cos(phi) + y * math.sin(phi), x * math.sin(phi) - y * math.cos(phi)
    variants = ((x, y, phi, 1, 0), (-x, y, -phi, -1, 0), (x, -y, -phi, 1, 1), (-x, -y, phi, -1, 1))
    back = ((xb, yb, phi, 1, 0), (-xb, yb, -phi, -1, 0), (xb, -yb, -phi, 1, 1), (-xb, -yb, phi, -1, 1))
    for (a, b, c, s, r) in variants:                                  # CSC
        q = _lpslp(a, b, c)
        if q:
            out.append((TYPES[14 + r], [s * q[0], s * q[1], s * q[2]]))
        q = _lpsrp(a, b, c)
        if q:
            out.append((TYPES[12 + r], [s * q[0], s * q[1], s * q[2]]))
    for (a, b, c, s, r) in variants:                                  # CCC
        q = _lprml(a, b, c)
        if q:
            out.append((TYPES[0 + r], [s * q[0], s * q[1], s * q[2]]))
    for (a, b, c, s, r) in back:
        q = _lprml(a, b, c)
        if q:
            out.append((TYPES[0 + r], [s * q[2], s * q[1], s * q[0]]))
    for (a, b, c, s, r) in variants:                                  # CCCC
        q = _lprupumrm(a, b, c)
        if q:
            out.append((TYPES[2 + r], [s * q[0], s * q[1], -s * q[1], s * q[2]]))
        q = _lprumlumrp(a, b, c)
        if q:
            out.append((TYPES[2 + r], [s * q[0], s * q[1], s * q[1], s * q[2]]))
    for (a, b, c, s, r) in variants:                                  # CCSC
        q = _lprmsmlm(a, b, c)
        if q:
            out.append((TYPES[4 + r], [s * q[0], -s * HALF_PI, s * q[1], s * q[2]]))
        q = _lprmsmrm(a, b, c)
        if q:
            out.append((TYPES[8 + r], [s * q[0], -s * HALF_PI, s * q[1], s * q[2]]))
    for (a, b, c, s, r) in back:
        q = _lprmsmlm(a, b, c)
        if q:
            out.append((TYPES[6 + r], [s * q[2], s * q[1], -s * HALF_PI, s * q[0]]))
        q = _lprmsmrm(a, b, c)
        if q:
            out.append((TYPES[10 + r], [s * q[2], s * q[1], -s * HALF_PI, s * q[0]]))
    for (a, b, c, s, r) in variants:                                  # CCSCC
        q = _lprmslmrp(a, b, c)
        if q:
            out.append((TYPES[16 + r], [s * q[0], -s * HALF_PI, s * q[1], -s * HALF_PI, s * q[2]]))
    return out


def reeds_shepp_all(start, goal, rho):
    """Every valid Reeds-Shepp candidate as a path in metres, shortest first (zero-length segments dropped)."""
    dx, dy = goal[0] - start[0], goal[1] - start[1]
    c, s = math.cos(start[2]), math.sin(start[2])
    x, y = (c * dx + s * dy) / rho, (-s * dx + c * dy) / rho
    phi = goal[2] - start[2]
    paths = []
    for word, ls in _candidates(x, y, phi):
        p = [(k, rho * v) for k, v in zip(word, ls) if abs(v) > 1e-10]
        if _close(endpoint(start, p, rho), goal, tol=1e-6 * max(1.0, rho)):
            paths.append(p)
    paths.sort(key=length)
    return paths


def reeds_shepp(start, goal, rho):
    """The shortest Reeds-Shepp path from start to goal (list of (kind, signed length in m))."""
    paths = reeds_shepp_all(start, goal, rho)
    return paths[0]


def word(path):
    """The path's word with + for forward and - for reverse segments, such as 'L+ S+ R-'."""
    return " ".join(f"{k}{'+' if s > 0 else '-'}" for k, s in path)


def cusps(path):
    """Number of direction reversals along the path."""
    signs = [1 if s > 0 else -1 for _, s in path]
    return sum(a != b for a, b in zip(signs, signs[1:]))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:                                             # self-check
        rng = np.random.default_rng(0)
        for _ in range(3000):
            st = (rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(-math.pi, math.pi))
            gl = (rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(-math.pi, math.pi))
            rho = rng.uniform(0.3, 3)
            rs = reeds_shepp(start=st, goal=gl, rho=rho)
            _, db = dubins(st, gl, rho)
            assert length(rs) <= length(db) + 1e-9
            assert length(rs) >= math.hypot(gl[0] - st[0], gl[1] - st[1]) - 1e-9
        assert abs(length(reeds_shepp((0, 0, 0), (3, 0, 0), 1)) - 3) < 1e-9
        assert abs(length(reeds_shepp((0, 0, 0), (-3, 0, 0), 1)) - 3) < 1e-9
        print("carpaths self-check passed")
