"""The running example of the frequency-response Notes (RO-063 to RO-065), shared by every figure script.

The robot of chapter RO-07 turns with yaw inertia I = 0.1 kg m^2 and a torque limit of 0.2 N m. Its heading loop is a
PD controller, kp = 0.4 N m/rad and kd = 0.08 N m s/rad; the derivative acts on the gyro's turn rate. Its speed plant is
m dv/dt = u - b v with m = 8 kg and b = 2 N s/m. Every number in the three Notes comes from the functions below
(no output when run on its own).
"""
import numpy as np
from scipy.optimize import brentq

M, B = 8.0, 2.0                 # speed plant: mass (kg) and rolling drag (N s/m)
I = 0.1                         # yaw inertia (kg m^2)
TAU_MAX = 0.2                   # turning torque limit (N m)
KP, KD = 0.4, 0.08              # PD heading gains (N m/rad, N m s/rad)
# RO-065's lead-lag heading controller: lead k (s + a)/(s + b) times lag (s + a2)/(s + b2)
K_LEAD, A_LEAD, B_LEAD = 1.875, 2.5 / 3, 7.5
A_LAG, B_LAG = 0.25, 0.025


def P_speed(s):
    """Speed plant: drive force (N) to speed (m/s)."""
    return 1 / (M * s + B)


def P_head(s):
    """Heading plant: turning torque (N m) to heading (rad)."""
    return 1 / (I * s ** 2)


def C_pd(s, kp=KP, kd=KD):
    return kp + kd * s


def C_lead(s, k=K_LEAD, a=A_LEAD, b=B_LEAD):
    return k * (s + a) / (s + b)


def C_lag(s, a=A_LAG, b=B_LAG):
    return (s + a) / (s + b)


def C_leadlag(s):
    return C_lead(s) * C_lag(s)


def L_head(s, tau=0.0, k=1.0, kp=KP, kd=KD):
    """Loop transfer function of the heading loop, with an optional delay tau (s) and gain factor k."""
    return k * C_pd(s, kp, kd) * P_head(s) * np.exp(-s * tau)


def G_yr(s, kp=KP, kd=KD):
    """Heading command to heading, derivative on the measured turn rate."""
    return kp / (I * s ** 2 + kd * s + kp)


def wn_zeta(kp=KP, kd=KD):
    return np.sqrt(kp / I), kd / (2 * np.sqrt(kp * I))


def db(x):
    return 20 * np.log10(np.abs(x))


def deg(x):
    return np.degrees(np.angle(x))


def peak(G, lo=1e-2, hi=1e2, n=400001):
    w = np.logspace(np.log10(lo), np.log10(hi), n)
    m = np.abs(G(1j * w))
    i = m.argmax()
    return w[i], m[i]


def bandwidth(G, lo=1e-3, hi=1e3):
    """Lowest frequency where the gain falls to 1/sqrt(2) of the zero-frequency gain."""
    g0 = abs(G(1e-9j))
    w = np.logspace(np.log10(lo), np.log10(hi), 600001)
    m = np.abs(G(1j * w))
    i = np.argmax(m < g0 / np.sqrt(2))
    return brentq(lambda x: abs(G(1j * x)) - g0 / np.sqrt(2), w[i - 1], w[i])


def margins(L, lo=1e-3, hi=1e3):
    """Gain crossover, phase margin (deg), delay margin (s), first phase crossover and gain margin of L(s)."""
    wgc = brentq(lambda x: abs(L(1j * x)) - 1, lo, hi)
    pm = 180 + deg(L(1j * wgc))
    pm = (pm + 180) % 360 - 180
    w = np.logspace(np.log10(lo), np.log10(hi), 800001)
    ph = np.unwrap(np.angle(L(1j * w)))
    idx = np.where(np.diff(np.sign(ph + np.pi)) != 0)[0]
    if len(idx):
        i = idx[0]
        wpc = brentq(lambda x: np.interp(np.log(x), np.log(w[i:i + 2]), ph[i:i + 2]) + np.pi, w[i], w[i + 1])
        gm = 1 / abs(L(1j * wpc))
    else:
        wpc, gm = np.inf, np.inf
    return dict(wgc=wgc, pm=pm, dm=np.radians(pm) / wgc, wpc=wpc, gm=gm)


def sens_peak(L, lo=1e-3, hi=1e3):
    w = np.logspace(np.log10(lo), np.log10(hi), 800001)
    d = np.abs(1 + L(1j * w))
    i = d.argmin()
    return w[i], d[i], 1 / d[i]


def winding(z, about=-1 + 0j):
    """Net counter-clockwise turns of the closed curve z (complex array) about the point 'about'."""
    a = np.unwrap(np.angle(z - about))
    return (a[-1] - a[0]) / (2 * np.pi)


def simulate_heading(t, ref, tau=0.0, kp=KP, kd=KD, dist=None, sat=True, ctrl=None):
    """Heading loop on a fixed 1 ms grid t: I theta'' = torque + dist(t). The controller sees the heading and turn
    rate tau seconds late. ctrl(e, rate, i) may replace the PD law (returns the torque). Returns heading, rate, torque."""
    dt = t[1] - t[0]
    n = len(t)
    lag = int(round(tau / dt))
    th, om, tq = np.zeros(n), np.zeros(n), np.zeros(n)
    r = ref(t) if callable(ref) else ref
    d = dist(t) if dist is not None else np.zeros(n)
    for i in range(n - 1):
        j = max(i - lag, 0)
        u = ctrl(r[i] - th[j], om[j], i) if ctrl else kp * (r[i] - th[j]) - kd * om[j]
        if sat:
            u = np.clip(u, -TAU_MAX, TAU_MAX)
        tq[i] = u
        om[i + 1] = om[i] + dt * (u + d[i]) / I
        th[i + 1] = th[i] + dt * om[i + 1]
    tq[-1] = tq[-2]
    return th, om, tq


def sine_fit(t, y, w):
    """Amplitude and phase (rad) of the best sine a sin(w t + phi) through y(t)."""
    A = np.column_stack([np.sin(w * t), np.cos(w * t), np.ones_like(t)])
    a, b, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    return np.hypot(a, b), np.arctan2(b, a)


def squeeze(z, r0=2.0, rmax=4.0):
    """Radial squeeze for drawing a Nyquist curve that runs off to infinity: points within r0 of the origin keep their
    place; farther points are pulled in so that infinity lands on the circle of radius rmax."""
    r = np.abs(z)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(r <= r0, r, r0 + (rmax - r0) * (r - r0) / (r - r0 + (rmax - r0)))
    return out * np.exp(1j * np.angle(z))


def nyquist_contour(eps=1e-3, R=1e4, n=4000):
    """The Nyquist contour, clockwise: up the imaginary axis (omega from eps to R), round the big arc, up from -R to
    -eps, and the small half circle that steps round the double pole at s = 0 on its right. Returns s and the part."""
    w = np.logspace(np.log10(eps), np.log10(R), n)
    parts = [(1j * w, "pos"), (R * np.exp(1j * np.linspace(np.pi / 2, -np.pi / 2, n // 4)), "arc"),
             (-1j * w[::-1], "neg"), (eps * np.exp(1j * np.linspace(-np.pi / 2, np.pi / 2, n // 4)), "small")]
    return np.concatenate([p for p, _ in parts]), np.concatenate([[k] * len(p) for p, k in parts])
