"""The robot's speed loop for RO-059 (no output when run on its own).

Plant: m dv/dt = u - b v - d (Newton's second law with rolling drag b v and a ramp's pull d), one Euler step per
10 ms control cycle. Controllers: open loop (a fixed force from the flat-floor calibration) and closed loop (that force
plus a correction K_p times the measured error). Every number the Note quotes comes from here via the notebook."""
import numpy as np

M = 8.0          # mass (kg)
B = 2.0          # rolling drag on a hard floor (N per m/s)
B_CARPET = 3.0   # rolling drag on carpet (N per m/s)
U_MAX = 4.0      # largest force the motors give, either way (N)
G = 9.81         # gravity (m/s^2)
DT = 0.01        # control cycle: 100 Hz (s)
V_REF = 0.5      # wanted speed (m/s)
KP = 20.0        # correction per m/s of error (N per m/s)
RISE = 0.01      # the ramp rises 1 cm per metre along it
D_RAMP = M * G * RISE          # the ramp's pull back down (N): 0.7848
X_RAMP = 2.0     # where the ramp starts (m); at 0.5 m/s the robots reach it at 4 s
SIGMA_N = 0.02   # encoder speed noise, one standard deviation (m/s)


def u_open(r):
    """The open-loop force: the flat-floor calibration, steady speed = u / b, so u = b r."""
    return B * r


def u_closed(r, y_m, kp=KP):
    """The closed-loop force: the open-loop force plus kp times the error r - y_m."""
    return B * r + kp * (r - y_m)


def run(T, closed, ramp=True, b_after=None, x_change=X_RAMP, ref=None, v0=V_REF, noise=0.0, seed=0, kp=KP):
    """Simulate T seconds at 100 Hz. ramp: the ramp's pull acts once x >= X_RAMP. b_after: drag from x_change on
    (the carpet). ref(t): the reference (default V_REF). Returns a dict of arrays, one entry per control cycle."""
    rng = np.random.default_rng(seed)
    n = int(round(T / DT))
    ref = ref or (lambda t: V_REF)
    v, x = v0, 0.0
    rows = []
    for k in range(n + 1):
        t = k * DT
        r = ref(t)
        y_m = v + noise * rng.standard_normal()                  # the sensor's reading: true speed plus noise
        u = u_closed(r, y_m, kp) if closed else u_open(r)
        u = float(np.clip(u, -U_MAX, U_MAX))                     # the actuator's limit
        d = D_RAMP if (ramp and x >= X_RAMP - 1e-9) else 0.0    # the disturbance
        b = b_after if (b_after is not None and x >= x_change - 1e-9) else B
        rows.append((t, x, v, y_m, r, r - y_m, u, d, b))
        a = (u - b * v - d) / M                                  # Newton: net force / mass
        x += v * DT
        v += a * DT                                              # one Euler step
    keys = ("t", "x", "v", "y_m", "r", "e", "u", "d", "b")
    arr = np.array(rows)
    return {k: arr[:, i] for i, k in enumerate(keys)}


def steady_open(d=0.0, b=B, r=V_REF):
    """Steady speed with the open-loop force: 0 = b r_cal - b v - d, with the controller's calibration b = 2."""
    return (u_open(r) - d) / b


def steady_closed(d=0.0, b=B, r=V_REF, kp=KP):
    """Steady speed in closed loop: 0 = B r + kp (r - v) - b v - d."""
    return (u_open(r) + kp * r - d) / (b + kp)


def ramp_ref(t, a=0.25, top=V_REF):
    """The tracking reference: speed up from rest at a m/s^2 to the top speed, then hold it."""
    return min(a * t, top)
