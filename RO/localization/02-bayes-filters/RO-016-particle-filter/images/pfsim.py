"""The running example of the particle-filter Note, shared by every figure script.

A robot drives along a corridor that loops round a block, 10 m around (position x from 0 to 10 m, and 10 m is 0 m
again). Three doors are set back into the right-hand wall: [1.5, 2.5], [4.0, 5.0] and [6.5, 7.5] m. A side range
sensor reads the distance to that wall: 1.0 m beside plain wall, 1.5 m in front of a door. Its noise has a standard
deviation of 0.15 m. Each move is commanded as 2.5 m; the wheels slip, so the true move has a standard deviation of
0.15 m. The robot starts at 2.1 m, in front of door 1, but does not know it.
"""
import numpy as np

LOOP = 10.0                                         # corridor length (m); position wraps round at 10 m
DOORS = [(1.5, 2.5), (4.0, 5.0), (6.5, 7.5)]        # door recesses (m)
WALL, DOOR = 1.0, 1.5                               # side distance to the wall, and into a door recess (m)
SIGMA_Z = 0.15                                      # sensor noise, standard deviation (m)
SIGMA_U = 0.15                                      # motion noise per move, standard deviation (m)
U = 2.5                                             # commanded move (m)

X_TRUE = [2.1, 4.62, 7.08]                          # true positions at the three readings (moves 2.52, 2.46 m)
Z = [1.46, 1.58, 1.41]                              # the three side readings (m)


def h(x):
    """Map: the side distance the sensor should read at position x (m)."""
    x = np.mod(x, LOOP)
    d = np.full(np.shape(x), WALL, dtype=float)
    for a, b in DOORS:
        d = np.where((x >= a) & (x <= b), DOOR, d)
    return d


def likelihood(z, x, sigma=SIGMA_Z):
    """Sensor model p(z | x): height of the normal curve centred on the expected reading h(x), at the reading z."""
    return np.exp(-0.5 * ((z - h(x)) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def move(x, u, rng, sigma=SIGMA_U):
    """Motion model, sampled: each particle moves u plus its own random slip, and wraps round the loop."""
    return np.mod(x + u + rng.normal(0, sigma, np.shape(x)), LOOP)


def low_variance(w, rng, r=None):
    """Low-variance (systematic) resampling: one random start r in [0, 1/M), then M pointers 1/M apart.
    Returns the index of the particle each pointer lands on."""
    M = len(w)
    c = np.cumsum(w / np.sum(w))
    if r is None:
        r = rng.uniform(0, 1 / M)
    pointers = r + np.arange(M) / M
    return np.searchsorted(c, pointers, side="right").clip(max=M - 1)


def multinomial(w, rng):
    """Plain resampling: M independent random draws, each picking particle i with probability w_i."""
    c = np.cumsum(w / np.sum(w))
    return np.searchsorted(c, rng.uniform(0, 1, len(w)), side="right").clip(max=len(w) - 1)


def run(M, rng, readings=Z, moves=(U, U)):
    """One run of the particle filter on the three readings. Returns the stages for plotting:
    a list of (name, particles, weights) after each step."""
    x = rng.uniform(0, LOOP, M)
    w = np.full(M, 1 / M)
    stages = [("start", x.copy(), w.copy())]
    for k, z in enumerate(readings):
        if k > 0:
            x = move(x, moves[k - 1], rng)
            w = np.full(M, 1 / M)
            stages.append((f"move {k}", x.copy(), w.copy()))
        w = likelihood(z, x)
        w = w / w.sum()
        stages.append((f"weigh {k + 1}", x.copy(), w.copy()))
        idx = low_variance(w, rng)
        x, w = x[idx], np.full(M, 1 / M)
        stages.append((f"resample {k + 1}", x.copy(), w.copy()))
    return stages


def grid_belief(readings=Z, moves=(U, U), n=2000):
    """Exact belief on a fine grid (a histogram filter with n cells), for comparison with the particles.
    Returns the cell centres, the predicted belief before each reading (None before the first) and the belief
    after each reading, both as densities (per m)."""
    xs = (np.arange(n) + 0.5) * LOOP / n
    dx = LOOP / n
    bel = np.full(n, 1 / LOOP)
    out, preds = [], [None]
    # motion kernel: normal with mean u, sd SIGMA_U, wrapped round the loop
    for k, z in enumerate(readings):
        if k > 0:
            shift = xs[:, None] - xs[None, :] - moves[k - 1]           # destination minus source minus u
            shift = (shift + LOOP / 2) % LOOP - LOOP / 2
            kern = np.exp(-0.5 * (shift / SIGMA_U) ** 2) / (SIGMA_U * np.sqrt(2 * np.pi))
            bel = kern @ bel * dx
            preds.append(bel.copy())
        bel = likelihood(z, xs) * bel
        bel = bel / (bel.sum() * dx)
        out.append(bel.copy())
    return xs, preds, out


def kidnap_run(inject, seed, M=200, T=60, kid=30, step=0.5):
    """A long run: the robot drives 0.5 m per step (slip sd 0.03 m) and reads at every step. At step `kid` it is
    picked up and put down 5 m further on (the kidnapped robot). After each resampling, a share `inject` of the
    particles is replaced by random ones spread evenly. Returns the error of the estimate at every step (m)."""
    rng = np.random.default_rng(seed)
    xt, x, errs = 2.1, rng.uniform(0, LOOP, M), []
    for t in range(T):
        if t > 0:
            xt = (xt + step + rng.normal(0, 0.03)) % LOOP
            if t == kid:
                xt = (xt + 5) % LOOP
            x = move(x, step, rng, 0.03)
        z = h(np.array([xt]))[0] + rng.normal(0, SIGMA_Z)
        w = likelihood(z, x)
        x = x[low_variance(w / w.sum(), rng)]
        k = int(round(inject * M))
        if k:
            x[rng.choice(M, k, replace=False)] = rng.uniform(0, LOOP, k)
        ang = np.angle(np.mean(np.exp(2j * np.pi * x / LOOP))) % (2 * np.pi)   # mean round the loop
        est = ang * LOOP / (2 * np.pi)
        errs.append(abs((est - xt + LOOP / 2) % LOOP - LOOP / 2))
    return np.array(errs)


if __name__ == "__main__":
    # self-checks
    assert h(np.array([2.0]))[0] == DOOR and h(np.array([3.0]))[0] == WALL and h(np.array([12.0]))[0] == DOOR
    w = np.array([0.1, 0.4, 0.2, 0.3])
    assert list(low_variance(w, None, r=0.05)) == [0, 1, 2, 3]
    xs, _, bels = grid_belief()
    for b in bels:
        assert abs(b.sum() * LOOP / len(xs) - 1) < 1e-9
    print("ok")
