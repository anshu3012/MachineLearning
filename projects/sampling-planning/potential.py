"""Potential fields (Choset slides; MR sec. 10.6; LaValle sec. 5.4.3), on any world.

The robot's height U is a bowl centred on the goal (the attractive potential) plus a hill round every obstacle and
every outer wall (the repulsive potential). The robot rolls downhill by gradient descent. Where the pull of the goal
and the push of an obstacle cancel, it stops: a local minimum. The randomized potential field then walks at random
until it is lower than the local minimum, and rolls on.

Only a Space is used: its blocked areas, bounds, robot radius, goal and free(p)."""
import numpy as np
import shapely
from shapely.geometry import LineString

ZETA = 1.0      # how steep the bowl is: U_att = 1/2 ZETA |q - goal|^2 (no unit)
ETA = 0.02      # how strongly an obstacle pushes (m^4, so U comes out in m^2)
QSTAR = 0.5     # influence distance (m): an obstacle farther than this does not push
ALPHA = 0.01    # gradient-descent step factor
MAXSTEP = 0.05  # longest descent step (m): near an obstacle the slope is steep and a long step could jump into it
DIAGONALS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # a random-walk step: x and y each +- one step


class Field:
    def __init__(self, space, goal=None):
        x0, y0, x1, y1 = space.bounds
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        walls = [LineString(corners[i:i + 2]) for i in range(4)]
        self.obstacles = np.array(list(space.blocked) + walls)
        for o in self.obstacles:
            shapely.prepare(o)
        self.space, self.r = space, space.radius
        self.goal = np.array(goal if goal is not None else space.goal, float)

    def clearance(self, xs, ys):
        """Clearances d_i (m) of the robot centred at each (x, y) to every obstacle: shape (obstacles, points)."""
        pts = shapely.points(np.ravel(xs), np.ravel(ys))
        return shapely.distance(self.obstacles[:, None], pts[None, :]) - self.r

    def U(self, xs, ys):
        """The height at points (x, y), in m^2: bowl + hills; infinite where the robot would touch an obstacle."""
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        d = self.clearance(xs, ys)
        with np.errstate(divide="ignore"):
            hills = np.where(d <= QSTAR, 0.5 * ETA * (1 / np.maximum(d, 1e-12) - 1 / QSTAR) ** 2, 0.0).sum(axis=0)
        att = 0.5 * ZETA * ((xs.ravel() - self.goal[0]) ** 2 + (ys.ravel() - self.goal[1]) ** 2)
        return np.where(d.min(axis=0) > 0, att + hills, np.inf).reshape(xs.shape)

    def u(self, q):
        return float(self.U(np.array([q[0]]), np.array([q[1]]))[0])

    def grad(self, q):
        """Gradient of U at q: ZETA (q - goal) for the bowl, and for each obstacle within QSTAR,
        -ETA (1/d - 1/QSTAR) / d^2 times the unit vector from the obstacle's nearest point to the robot."""
        q = np.asarray(q, float)
        g = ZETA * (q - self.goal)
        p = shapely.points(q[0], q[1])
        d = shapely.distance(self.obstacles, p) - self.r
        for o, di in zip(self.obstacles[d <= QSTAR], d[d <= QSTAR]):
            (ax, ay), (bx, by) = shapely.shortest_line(o, p).coords
            n = np.array([bx - ax, by - ay]) / (di + self.r)
            g -= ETA * (1 / di - 1 / QSTAR) / di ** 2 * n
        return g

    def descend(self, q0, n_max=20000, tol=1e-5, goal_tol=0.02):
        """Gradient descent: q <- q - ALPHA grad U, each step at most MAXSTEP long. Stops within goal_tol of the goal
        or when a step is shorter than tol (a minimum). Returns the points, shape (n, 2)."""
        q = np.array(q0, float)
        pts = [q]
        for _ in range(n_max):
            s = -ALPHA * self.grad(q)
            length = np.hypot(*s)
            if length > MAXSTEP:
                s *= MAXSTEP / length
            q = q + s
            pts.append(q)
            if np.hypot(*(q - self.goal)) < goal_tol or np.hypot(*s) < tol:
                break
        return np.array(pts)

    def at_goal(self, q, tol=0.05):
        return np.hypot(*(np.asarray(q) - self.goal)) <= tol

    def random_walk(self, q0, u_stop, rng, n_steps, step):
        """Each step moves x and y by +-step (a coin toss each); a step the robot cannot stand at is thrown away and
        tried again (here: the four moves in random order, the first free one taken; none free ends the walk). Stops
        early once U is below u_stop. Returns the points."""
        q = np.array(q0, float)
        pts = [q]
        for _ in range(n_steps):
            for i in rng.permutation(4):
                nq = q + step * np.array(DIAGONALS[i])
                if self.space.free(nq):
                    break
            else:
                break
            q = nq
            pts.append(q)
            if self.u(q) < u_stop:
                break
        return np.array(pts)

    def randomized(self, q0, rng, step, walk_len=(100, 400), k_walks=20, max_walks=200):
        """The randomized potential field (LaValle sec. 5.4.3, Figure 5.15): descend; when stuck, random walk, then
        descend again; after k_walks walks that all fall back to the same height, restart from a random point of an
        earlier walk. Returns a list of (mode, points), mode "descend", "walk" or "backtrack"."""
        parts = [("descend", self.descend(q0))]
        q = parts[-1][1][-1]
        fails, walk_pts, walks = 0, [], 0
        while not self.at_goal(q) and walks < max_walks:
            u_stuck = self.u(q)
            w = self.random_walk(q, u_stuck, rng, int(rng.integers(walk_len[0], walk_len[1] + 1)), step)
            walks += 1
            walk_pts.extend(w[1:])
            parts.append(("walk", w))
            d = self.descend(w[-1])
            parts.append(("descend", d))
            q = d[-1]
            if self.at_goal(q):
                break
            if self.u(q) < u_stuck - 1e-6:  # a lower local minimum: start counting again from there
                fails = 0
                continue
            fails += 1
            if fails >= k_walks:
                b = walk_pts[int(rng.integers(len(walk_pts)))]
                parts.append(("backtrack", np.array([q, b])))
                d = self.descend(b)
                parts.append(("descend", d))
                q, fails = d[-1], 0
        return parts


def path_length(P):
    P = np.asarray(P)
    return float(np.hypot(*np.diff(P, axis=0).T).sum())
