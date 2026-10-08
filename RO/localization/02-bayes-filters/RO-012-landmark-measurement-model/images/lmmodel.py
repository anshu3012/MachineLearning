"""Shared numbers and functions for this Note's figures (no output when run on its own).
The 5 m x 4 m room with three landmarks (coloured poles) at known places. The robot stands at pose A = (2, 2, 0).
Each reading is (range r, bearing phi, signature s); noise spreads sigma_r = 0.1 m, sigma_phi = 5 degrees."""
import numpy as np

LM = {"pink": (4.4, 3.8), "green": (0.4, 3.2), "blue": (3.2, 0.4)}
POSE_A = (2.0, 2.0, 0.0)
SIG_R = 0.1
SIG_PHI = np.radians(5)
READ = {"pink": (3.10, np.radians(40)), "green": (1.95, np.radians(141)), "blue": (2.05, np.radians(-55))}


def wrap(a):
    """Angle wrapped to (-pi, pi]."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def expected(pose, m):
    x, y, th = pose
    dx, dy = m[0] - x, m[1] - y
    return np.hypot(dx, dy), wrap(np.arctan2(dy, dx) - th)


def gauss(v, sig):
    return np.exp(-0.5 * (v / sig) ** 2) / (sig * np.sqrt(2 * np.pi))


def landmark_density(pose, name, reading=None):
    r, phi = reading or READ[name]
    rh, ph = expected(pose, LM[name])
    return gauss(r - rh, SIG_R) * gauss(wrap(phi - ph), SIG_PHI)


def range_density_xy(X, Y, name):
    """Range part only, over positions (x, y): high on a ring of radius r around the landmark."""
    m = LM[name]
    return gauss(READ[name][0] - np.hypot(m[0] - X, m[1] - Y), SIG_R)


def sample_poses(name, n, rng):
    """Poses consistent with one reading of landmark `name` (Thrun Table 6.5)."""
    m = LM[name]
    r, phi = READ[name]
    g = rng.uniform(0, 2 * np.pi, n)
    rr = r + rng.normal(0, SIG_R, n)
    pp = phi + rng.normal(0, SIG_PHI, n)
    return m[0] + rr * np.cos(g), m[1] + rr * np.sin(g), wrap(g + np.pi - pp)
