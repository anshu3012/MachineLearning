"""The table-top world of this Note and its task and motion planner (no output when run on its own).

Copied and extended from RO-053's manip.py (side view of one vertical plane): the 2R arm with links of 0.3 m and
0.2 m, shoulder at (0, 0), table top 0.1 m below the shoulder, a suction gripper that holds an object by its flat top
and a wrist that keeps it upright, so a held object hangs straight below the hand. New here: two movable objects,
the cup (6 cm wide, 8 cm tall) and the bottle (4 cm wide, 14 cm tall, flat cap), and the part of the table where
objects may stand, x from 0.05 m (where the robot's top ends) to 0.60 m.

The planner follows the "sequence before satisfy" strategy of Garrett et al. 2021, section 3.3.1, with negative
feedback (section 3.4.2): a forward search over actions (RO-035) proposes a plan skeleton, a backtracking search
fills in its continuous values with samplers and tests like PDDLStream's continuous_tamp streams (s-region, s-ik,
s-motion, t-cfree), and a failed test becomes a fact the next forward search must respect."""
import heapq
from collections import deque

import numpy as np
import shapely
from scipy.spatial import cKDTree
from shapely.geometry import box

L1, L2 = 0.3, 0.2                     # link lengths (m), as in RO-036 and RO-053
TOP = -0.10                           # height of the table top and of the robot's top (m)
TABLE = (0.05, 0.60)                  # where objects may stand on the table (m)
SIZE = {"cup": (0.06, 0.08), "bottle": (0.04, 0.14)}   # width, height (m)
A_X, B_X = 0.18, 0.42                 # the cup's spot A and the goal spot B (m), as in RO-053
HOME = (90.0, 0.0)                    # the arm straight up
TOUCH = 1e-3                          # touching is allowed (at a grasp or a placing), overlapping is not (m)


def floor():
    return box(-1.0, -1.0, 1.0, TOP)


def standing(o, x):
    w, h = SIZE[o]
    return box(x - w / 2, TOP, x + w / 2, TOP + h)


def hanging(o, hand):
    w, h = SIZE[o]
    return box(hand[0] - w / 2, hand[1] - h, hand[0] + w / 2, hand[1])


def top(o, x):
    """Where the hand must be to hold object o standing at x: the centre of its flat top (the one grasp)."""
    return (x, TOP + SIZE[o][1])


def fk(t1, t2):
    a1, a12 = np.radians(t1), np.radians(np.asarray(t1) + np.asarray(t2))
    ex, ey = L1 * np.cos(a1), L1 * np.sin(a1)
    return (ex, ey), (ex + L2 * np.cos(a12), ey + L2 * np.sin(a12))


def wrap(t):
    return (np.asarray(t) + 180.0) % 360.0 - 180.0


def ik(p):
    """Both joint-angle solutions (degrees) that put the hand at p, or [] if p is out of reach."""
    x, y = p
    c2 = (x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if abs(c2) > 1:
        return []
    out = []
    for s in (1, -1):
        t2 = s * np.degrees(np.arccos(c2))
        k1, k2 = L1 + L2 * np.cos(np.radians(t2)), L2 * np.sin(np.radians(t2))
        t1 = np.degrees(np.arctan2(y, x) - np.arctan2(k2, k1))
        out.append((float(wrap(t1)), float(wrap(t2))))
    return out


class World:
    """Where each object stands (x of its bottom centre) and what the hand holds."""

    def __init__(self, at, held=None):
        self.at, self.held = dict(at), held

    def copy(self):
        return World(self.at, self.held)

    def obstacles(self):
        return shapely.union_all([floor()] + [standing(o, x).buffer(-TOUCH) for o, x in self.at.items()])

    def collide(self, t1, t2):
        """True where the links (and a held object) overlap the table or a standing object."""
        t1, t2 = np.atleast_1d(t1).astype(float), np.atleast_1d(t2).astype(float)
        (ex, ey), (hx, hy) = fk(t1, t2)
        O = self.obstacles()
        shapely.prepare(O)
        z = np.zeros_like(t1)
        link1 = shapely.linestrings(np.stack([np.stack([z, z], 1), np.stack([ex, ey], 1)], 1))
        link2 = shapely.linestrings(np.stack([np.stack([ex, ey], 1), np.stack([hx, hy], 1)], 1))
        hit = shapely.intersects(O, link1) | shapely.intersects(O, link2)
        if self.held:
            w, h = SIZE[self.held]
            held = shapely.box(hx - w / 2, hy - h, hx + w / 2, hy)
            env = shapely.union_all([floor().buffer(-TOUCH)] + [standing(o, x) for o, x in self.at.items()])
            shapely.prepare(env)
            hit |= shapely.intersects(env, held) | shapely.intersects(held, link1)
        return hit


# ---------- the samplers and tests (PDDLStream continuous_tamp: s-region, s-ik, s-motion, t-cfree) ----------

def sample_place(o, rng):
    """s-region: a random x on the table at which object o stands with its whole base on the table."""
    w = SIZE[o][0]
    return float(rng.uniform(TABLE[0] + w / 2, TABLE[1] - w / 2))


def cfree(o1, x1, o2, x2):
    """t-cfree: True if o1 standing at x1 and o2 standing at x2 do not overlap (touching allowed)."""
    return not standing(o1, x1).buffer(-TOUCH).intersects(standing(o2, x2))


def grasp_conf(world, o, x):
    """s-ik: a collision-free joint configuration with the hand on top of o at x, in `world` (the elbow-up one
    first), or None (out of reach, or both solutions collide)."""
    for q in sorted(ik(top(o, x)), key=lambda q: -q[1] if q[1] < 0 else 999):
        if not world.collide(*q)[0]:
            return q
    return None


def angdiff(a, b):
    return wrap(np.asarray(b) - np.asarray(a))


def dist(a, b):
    d = angdiff(a, b)
    return float(np.hypot(*d)) if np.ndim(d) == 1 else np.hypot(d[..., 0], d[..., 1])


def interp(a, b, n):
    d = angdiff(a, b)
    t = np.linspace(0, 1, n)[:, None]
    return wrap(np.asarray(a) + t * d)


def seg_free(world, a, b, step=1.0):
    n = max(2, int(np.ceil(dist(a, b) / step)) + 1)
    P = interp(a, b, n)
    return not world.collide(P[:, 0], P[:, 1]).any()


def motion(world, s, g, n=150, k=10, seed=0):
    """s-motion: the PRM of RO-052 in the arm's C-space (a torus), copied from RO-053: n free milestones, k nearest
    by the wrap-around distance, A* from s to g. Returns (path, length in degrees) or (None, inf)."""
    if seg_free(world, s, g):
        return [tuple(s), tuple(g)], dist(s, g)
    rng = np.random.default_rng(seed)
    V = []
    while len(V) < n:
        q = rng.uniform(-180, 180, 2)
        if not world.collide(q[0], q[1])[0]:
            V.append(tuple(q))
    V = V + [tuple(s), tuple(g)]
    A = np.asarray(V)
    off = np.array([(i, j) for i in (-360, 0, 360) for j in (-360, 0, 360)])
    tree = cKDTree((A[None, :, :] + off[:, None, :]).reshape(-1, 2))
    E, tried = {}, set()
    for i in range(len(V)):
        _, idx = tree.query(A[i], k=k + 1)
        for jj in idx[1:]:
            j = jj % len(V)
            key = (min(i, j), max(i, j))
            if j == i or key in tried:
                continue
            tried.add(key)
            if seg_free(world, V[i], V[j]):
                E[key] = dist(V[i], V[j])
    nbr = {i: [] for i in range(len(V))}
    for (i, j), d in E.items():
        nbr[i].append((j, d))
        nbr[j].append((i, d))
    si, gi = len(V) - 2, len(V) - 1
    best, par, pq, done = {si: 0.0}, {si: None}, [(dist(V[si], V[gi]), si)], set()
    while pq:
        _, i = heapq.heappop(pq)
        if i in done:
            continue
        done.add(i)
        if i == gi:
            break
        for j, d in nbr[i]:
            if best[i] + d < best.get(j, np.inf):
                best[j], par[j] = best[i] + d, i
                heapq.heappush(pq, (best[j] + dist(V[j], V[gi]), j))
    if gi not in done:
        return None, np.inf
    path = [gi]
    while par[path[-1]] is not None:
        path.append(par[path[-1]])
    return [V[i] for i in path[::-1]], best[gi]


def densify(path, step=2.0):
    out = [tuple(path[0])]
    for a, b in zip(path, path[1:]):
        n = max(2, int(np.ceil(dist(a, b) / step)) + 1)
        out += [tuple(p) for p in interp(a, b, n)[1:]]
    return out


# ---------- the task level: forward search over facts (RO-035), with poses as names ----------
# A pose is a name: "A", "B", "start" (where the bottle stands at first) or "new" (a place on the table whose x the
# value search will sample). The task level knows no geometry: it assumes every placement is free, except the
# collisions it has been told about (facts learned from failed tests).

POSES = {"cup": ["A", "B", "new"], "bottle": ["start", "new"]}


def task_plans(start, goal, blocked, max_len=6):
    """Breadth-first forward search (RO-035) over states {object: pose name or 'held'}; yields every plan skeleton
    in order of length. blocked: set of (o1, pose1, o2, pose2) placements known to collide."""
    key = lambda s: tuple(sorted(s.items()))
    q = deque([(start, [])])
    seen = {key(start): 0}
    while q:
        s, plan = q.popleft()
        if all(s.get(o) == p for o, p in goal.items()):
            yield plan
            continue
        if len(plan) >= max_len:
            continue
        held = [o for o, p in s.items() if p == "held"]
        acts = []
        if not held:
            acts = [("pick", o, p) for o, p in s.items()]
        else:
            o = held[0]
            for p in POSES[o]:
                if any((o, p, o2, p2) in blocked for o2, p2 in s.items() if o2 != o):
                    continue
                acts.append(("place", o, p))
        for a in acts:
            n = dict(s)
            n[a[1]] = "held" if a[0] == "pick" else a[2]
            if seen.get(key(n), 99) < len(plan) + 1:
                continue
            seen[key(n)] = len(plan) + 1
            q.append((n, plan + [a]))


NAMED_X = {("cup", "A"): A_X, ("cup", "B"): B_X, ("bottle", "start"): B_X}


def solve_values(world, names, plan, rng, max_samples=20, log=None):
    """Backtracking search for the plan's continuous values: each pick needs a grasp configuration (s-ik) and a
    transit motion (s-motion); each place needs a placement (named, or sampled by s-region for "new"), a free
    placement (t-cfree), a configuration (s-ik) and a transfer motion. Returns (steps, None) on success, or
    (None, failure) with the failed test of a named placement. log collects every test, in order."""
    log = log if log is not None else []

    def rec(i, w, q, steps, names):
        if i == len(plan):
            return steps, None
        kind, o, p = plan[i]
        if kind == "pick":
            x = w.at[o]
            g = grasp_conf(w, o, x)
            if g is None:
                log.append(dict(step=i, test="ik", ok=False, o=o, x=x))
                return None, ("ik", o, names[o])
            path, L = motion(w, q, g)
            log.append(dict(step=i, test="motion", ok=path is not None, o=o, x=x, length=L))
            if path is None:
                return None, ("motion", o, names[o])
            n = w.copy()
            del n.at[o]
            n.held = o
            nn = dict(names)
            nn[o] = "held"
            return rec(i + 1, n, g, steps + [dict(kind=kind, o=o, x=x, q=g, path=path, length=L, world=w)], nn)
        # place
        tries = 1 if p != "new" else max_samples
        fail = None
        for _ in range(tries):
            x = NAMED_X[(o, p)] if p != "new" else sample_place(o, rng)
            entry = dict(step=i, o=o, x=x, sampled=p == "new")
            bad = [o2 for o2, x2 in w.at.items() if not cfree(o, x, o2, x2)]
            if bad:
                log.append(dict(entry, test="cfree", ok=False, other=bad[0]))
                fail = ("cfree", o, p, bad[0], names[bad[0]])
                continue
            n = w.copy()
            n.held, n.at[o] = None, x
            g = grasp_conf(n, o, x)
            if g is None:
                log.append(dict(entry, test="ik", ok=False))
                fail = ("ik", o, p)
                continue
            path, L = motion(w, q, g)
            if path is None:
                log.append(dict(entry, test="motion", ok=False))
                fail = ("motion", o, p)
                continue
            log.append(dict(entry, test="motion", ok=True, length=L))
            nn = dict(names)
            nn[o] = p
            res, f = rec(i + 1, n, g, steps + [dict(kind=kind, o=o, x=x, q=g, path=path, length=L, world=w)], nn)
            if res is not None:
                return res, None
            log.append(dict(entry, test="backtrack", ok=False, why=f))
            fail = f
        return None, fail

    return rec(0, world, HOME, [], dict(names))


def tamp(world, start, goal, seed=0, max_skeletons=10):
    """Sequence before satisfy with negative feedback: returns (solution steps, history of skeletons tried, log)."""
    rng = np.random.default_rng(seed)
    blocked, history, log = set(), [], []
    for _ in range(max_skeletons):
        plan = next(task_plans(start, goal, blocked), None)
        if plan is None:
            break
        steps, fail = solve_values(world, start, plan, rng, log=log)
        history.append(dict(plan=plan, fail=fail, blocked=set(blocked)))
        if steps is not None:
            return steps, history, log
        if fail and fail[0] == "cfree" and "new" not in (fail[2], fail[4]):   # both places named: a new fact
            blocked.add((fail[1], fail[2], fail[3], fail[4]))
    return None, history, log


if __name__ == "__main__":
    w0 = World({"cup": A_X, "bottle": B_X})
    steps, hist, log = tamp(w0, {"cup": "A", "bottle": "start"}, {"cup": "B"})
    for h in hist:
        print(h)
    for e in log:
        print(e)
    for s in steps:
        print(s["kind"], s["o"], round(s["x"], 4), np.round(s["q"], 1), round(s["length"], 1))


# ---------- SayCan's "Can": an affordance for each skill, from the tests above ----------

SKILLS = ["pick up the cup", "pick up the bottle", "put down the cup on spot B", "put down the cup on the table",
          "put down the bottle on spot B", "put down the bottle on the table", "done"]
DONE_AFFORDANCE = 0.1                 # SayCan gives "done" a small fixed affordance (Ahn et al. 2022, App. D.2)


def try_skill(world, q, skill, rng, max_samples=20):
    """Run the tests of one skill in the current world. Returns (affordance, new world, new q, x or None):
    1 if the tests find a placement, a configuration and a motion, else 0. "on the table" means a free place
    anywhere on the table outside spot B, sampled with s-region."""
    if skill == "done":
        return DONE_AFFORDANCE, world, q, None
    words = skill.split()
    o = words[3]
    if skill.startswith("pick up"):
        if world.held is not None or o not in world.at:
            return 0.0, world, q, None
        g = grasp_conf(world, o, world.at[o])
        if g is None or motion(world, q, g)[0] is None:
            return 0.0, world, q, None
        n = world.copy()
        x = n.at.pop(o)
        n.held = o
        return 1.0, n, g, x
    if world.held != o:
        return 0.0, world, q, None
    on_b = skill.endswith("spot B")
    for _ in range(1 if on_b else max_samples):
        x = B_X if on_b else sample_place(o, rng)
        if not on_b and not cfree(o, x, "cup", B_X):
            continue
        if any(not cfree(o, x, o2, x2) for o2, x2 in world.at.items()):
            continue
        n = world.copy()
        n.held, n.at[o] = None, x
        g = grasp_conf(n, o, x)
        if g is None or motion(world, q, g)[0] is None:
            continue
        return 1.0, n, g, x
    return 0.0, world, q, None
