"""RO-065's own helpers on top of loopkit (no output when run on its own): the lead and lag families used in the
loop-shaping animations, the heading loop simulated with any of the controllers, and the gain curves of the Gang of
Four. Controllers act on the heading error e = reference - measured heading.
"""
import numpy as np

from loopkit import (A_LAG, A_LEAD, B_LAG, B_LEAD, I, K_LEAD, KD, KP, TAU_MAX, C_lag, C_lead, C_leadlag, C_pd,
                     P_head, margins, sens_peak)

W_C = 2.5                       # crossover the lead is centred on (rad/s)
DRAG = 0.02                     # drag torque: one wheel drags 0.2 N more, 0.1 m from the centre (N m)
I_PAY, TAU_REAL = 0.15, 0.25    # the real robot: payload inertia (kg m^2) and motor-driver delay (s)


def lead_family(r, wc=W_C):
    """Lead k (s + a)/(s + b) with b/a = r, centred on wc (sqrt(ab) = wc) and scaled so that |L(j wc)| = 1."""
    a, b = wc / np.sqrt(r), wc * np.sqrt(r)
    k = 1 / (abs((1j * wc + a) / (1j * wc + b)) * abs(P_head(1j * wc)))
    return k, a, b


def lag_family(r, a2=A_LAG):
    """Lag (s + a2)/(s + b2) with a2/b2 = r (r = inf gives b2 = 0, the PI case)."""
    return a2, (0.0 if np.isinf(r) else a2 / r)


def controllers():
    """The controllers compared in the Note, as functions of s."""
    return {"PD, kd = 0.08": lambda s: C_pd(s),
            "PD, kd = 0.4": lambda s: C_pd(s, KP, 0.4),
            "lead": lambda s: C_lead(s),
            "lead-lag": lambda s: C_leadlag(s)}


def gang_of_four(C, w, inertia=I):
    s = 1j * w
    P = 1 / (inertia * s ** 2)
    L = P * C(s)
    S = 1 / (1 + L)
    return dict(S=S, T=L * S, PS=P * S, CS=C(s) * S, L=L)


def sim(kind, t, dist=0.0, t_dist=1.0, ref=0.0, inertia=I, tau=0.0, sat=True, b_lag=B_LAG):
    """Heading loop on the 1 ms grid t. kind: 'pd', 'pd04', 'lead' or 'leadlag'. A drag torque `dist` (N m) starts at
    t_dist; the controller sees the heading tau seconds late; b_lag sets the lag's pole (zero fixed at 0.25 rad/s).
    Returns heading (rad) and torque (N m)."""
    dt = t[1] - t[0]
    n, lag = len(t), int(round(tau / dt))
    th, om, tq = np.zeros(n), np.zeros(n), np.zeros(n)
    x1 = x2 = 0.0
    d = np.where(t >= t_dist, dist, 0.0)
    for i in range(n - 1):
        j = max(i - lag, 0)
        e = ref - th[j]
        if kind in ("pd", "pd04"):
            u = KP * e - (KD if kind == "pd" else 0.4) * om[j]
        else:
            u1 = K_LEAD * e + K_LEAD * (A_LEAD - B_LEAD) * x1          # lead: k e + k (a - b)/(s + b) e
            x1 += dt * (-B_LEAD * x1 + e)
            u = u1 if kind == "lead" else u1 + (A_LAG - b_lag) * x2      # lag: u1 + (a2 - b2)/(s + b2) u1
            x2 += dt * (-b_lag * x2 + u1)
        if sat:
            u = np.clip(u, -TAU_MAX, TAU_MAX)
        tq[i] = u
        om[i + 1] = om[i] + dt * (u + d[i]) / inertia
        th[i + 1] = th[i] + dt * om[i + 1]
    tq[-1] = tq[-2]
    return th, tq
