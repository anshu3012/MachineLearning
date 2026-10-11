"""Map-consistent sampling. A wall (grey box, y from 1.45 to 1.53 m, x from 1.7 to 2.8 m) lies across the cloud of the
Note's odometry step. Left: one big step, samples inside the wall are rejected (red), but samples beyond the wall
(purple) are free and still kept, although the robot cannot drive through the wall. Right: the same motion in twenty small
steps with the noise per step raised so the total spread is the same, rejecting and redrawing at each step: no
sample gets beyond the wall. Seeded. The functions behind Figure 9 (map_reject_anim.py) and the notebook."""

import numpy as np
from motion import A_ODO, START, sample_odometry

WALL = (1.7, 2.8, 1.45, 1.53)
inside = lambda x, y: (x > WALL[0]) & (x < WALL[1]) & (y > WALL[2]) & (y < WALL[3])
beyond = lambda x, y: (x > WALL[0]) & (x < WALL[1]) & (y >= WALL[3])


def big_step(rng, n=500):
    return sample_odometry((0.500, 0.479, 0.500), START, rng, n)


def small_steps(rng, n=500, k=20):
    """k sub-steps along the arc; any sample that lands in the wall is redrawn from its previous pose."""
    x, y, th = (np.full(n, v) for v in START)
    u = (0.5 / k, 0.479 / k, 0.5 / k)                 # one k-th of the turn and of the arc
    a = tuple(np.sqrt(k) * v for v in A_ODO)          # noise per sub-step raised so the total spread matches one big step
    for _ in range(k):
        nx, ny, nth = sample_odometry(u, (x, y, th), rng, n, a)
        bad = inside(nx, ny)
        while bad.any():
            rx, ry, rth = sample_odometry(u, (x[bad], y[bad], th[bad]), rng, bad.sum(), a)
            nx[bad], ny[bad], nth[bad] = rx, ry, rth
            bad = inside(nx, ny)
        x, y, th = nx, ny, nth
    return x, y, th



if __name__ == "__main__":
    bx, by, _ = big_step(np.random.default_rng(5))
    sx, sy, _ = small_steps(np.random.default_rng(5))
    print("big step: inside wall", inside(bx, by).sum(), " beyond wall", beyond(bx, by).sum(),
          "  small steps: beyond wall", beyond(sx, sy).sum())
