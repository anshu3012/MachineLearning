"""The robot's heading loop for RO-060 (no output when run on its own).

Plant: I dw/dt = tau + tau_d, dth/dt = w (Newton's second law for turning: torque = moment of inertia x angular
acceleration). The torque is held for each 10 ms control cycle, so each step is exact for a constant torque. While it
turns, the robot drives forward at 0.5 m/s (the kinematic model of RO-001, one Euler step per cycle).
Controller: tau = kp e + ki (sum of e dt) + kd (e - e_prev) / dt, the error e = th_ref - th, clipped to +-0.2 N m.
Every number the Note quotes comes from here via the notebook."""
import numpy as np

I = 0.1             # moment of inertia about the vertical axis (kg m^2)
M = 8.0             # mass (kg)
TAU_MAX = 0.2       # largest turning torque, either way (N m)
DT = 0.01           # control cycle: 100 Hz (s)
V = 0.5             # forward speed while turning (m/s), held by the speed loop of RO-059
TH_REF = np.pi / 4  # the new heading after the corner: 45 degrees (rad)
KP = 0.2            # proportional gain (N m per rad)
KD = 0.283          # derivative gain (N m per rad/s)
KI = 0.05           # integral gain (N m per rad s)
TAU_DRAG = -0.02    # a dragging right gearbox: a steady torque turning the robot right (N m)


def run(T, kp=KP, kd=0.0, ki=0.0, tau_d=0.0, inertia=I, th_ref=TH_REF, tau_max=TAU_MAX):
    """Simulate T seconds at 100 Hz from heading 0, at rest in turning. Returns a dict of arrays, one per cycle."""
    n = int(round(T / DT))
    th = w = x = y = 0.0
    integ, e_prev = 0.0, None
    rows = []
    for k in range(n + 1):
        t = k * DT
        e = th_ref - th
        integ += e * DT                                       # the running sum of the error, this cycle included
        de = 0.0 if e_prev is None else (e - e_prev) / DT     # first cycle: no previous error, no derivative
        p_t, i_t, d_t = kp * e, ki * integ, kd * de
        tau = float(np.clip(p_t + i_t + d_t, -tau_max, tau_max))
        rows.append((t, th, w, e, de, integ, p_t, i_t, d_t, tau, x, y))
        alpha = (tau + tau_d) / inertia                       # Newton for turning
        x += V * np.cos(th) * DT
        y += V * np.sin(th) * DT
        th += w * DT + 0.5 * alpha * DT * DT                  # exact for a torque held over the cycle
        w += alpha * DT
        e_prev = e
    keys = ("t", "th", "w", "e", "de", "integ", "p", "i", "d", "tau", "x", "y")
    arr = np.array(rows)
    return {k: arr[:, j] for j, k in enumerate(keys)}


def peaks(a):
    """Times and values of the local maxima of the heading."""
    th = a["th"]
    idx = [j for j in range(1, len(th) - 1) if th[j] > th[j - 1] and th[j] >= th[j + 1]]
    return a["t"][idx], th[idx]


def within(a, deg=1.0, ref=TH_REF):
    """The time after which the heading stays within deg degrees of ref (None if it never does)."""
    off = np.abs(np.degrees(a["th"] - ref)) > deg
    if off[-1]:
        return None
    last = np.where(off)[0]
    return a["t"][last[-1] + 1] if len(last) else 0.0


def spin_up(torque=TAU_MAX, inertia=I, T=1.0):
    """A constant torque from rest: angular acceleration, turn rate and angle after T seconds."""
    alpha = torque / inertia
    return alpha, alpha * T, 0.5 * alpha * T * T
