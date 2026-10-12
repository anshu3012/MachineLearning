"""RO-074's additions to the chapter's tracker kit (trackkit.py, copied from RO-071 and RO-072): RO-070's line rule
with and without the curve's feedforward turn, the tracker metrics, and a course with a tighter arc (no output when
imported; run it on its own for its self-check).

The line rule (RO-070's demonstration driver, RO-069's rule on the course's tangent at the nearest point, rear axle):
turn rate w = -K_D e - K_H th_e, with K_D = 0.5 rad/s per m and K_H = 2 per s, turned into steering by the bicycle
model, tan(delta) = L w / v. At 2 m/s it is critically damped (spring v K_D = 1, damper 2).
Feedforward: the turn the course itself needs, v kappa, added to w; on the course, with no error, the steering is then
atan(L kappa), 14.04 degrees on the 10 m arc (Boyali et al. 2018, eq. 33).
Metrics (at the rear axle for every tracker): RMS lateral error over the whole run; peak lateral error, the largest |e|;
steering travel, the sum of the changes of the steering command from tick to tick, in degrees (how far the steering
wheel is turned back and forth in total); reach, the course distance where |e| first falls below 0.1 m.
"""
import numpy as np

import trackkit as tk

K_D, K_H = 0.5, 2.0                       # rad/s per m, per s


def line_rule(x, y, th, v, ff=False, kd=K_D, kh=K_H):
    s, e, the, kap = tk.errors(x, y, th)
    w_ff = v * kap if ff else 0.0
    w = w_ff - kd * e - kh * the
    return dict(delta=float(np.arctan(tk.L * w / v)), w=w, w_ff=w_ff, s=s, e=e, the=the, kappa=kap)


def set_arc(r):
    """Change the course's arc radius (the straights stay 10 m); returns the old radius."""
    old = tk.R_ARC
    tk.R_ARC = r
    tk.S2 = tk.S1 + np.pi / 2 * r
    tk.S_END = tk.S2 + 10.0
    tk.S_MID = (tk.S1 + tk.S2) / 2
    return old


def scores(run):
    """RMS lateral error (m), peak lateral error (m), steering travel (deg), distance to get within 0.1 m (m)."""
    e, s = run["e"], run["s"]
    below = np.abs(e) < 0.1
    cmds = np.array([0.0] + [t["delta_cmd"] for t in run["ticks"]])
    return dict(rms=float(np.sqrt(np.mean(e ** 2))), peak=float(np.abs(e).max()),
                travel=float(np.degrees(np.abs(np.diff(cmds)).sum())),
                reach=float(s[np.argmax(below)]) if below.any() else np.nan)


def steady_offset(v=2.0, kd=K_D, r=10.0):
    """The line rule without feedforward on an arc of radius r: the lateral error e (+ = left, towards the centre)
    at which -kd e (heading error 0) equals the turn the rear axle's circle needs, v / (r - e)."""
    lo, hi = -5.0, 0.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if -kd * mid - v / (r - mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    assert abs(np.degrees(np.arctan(tk.L * 0.1)) - 14.036) < 1e-3
    assert abs(steady_offset() + 0.385) < 1e-3 and abs(steady_offset(v=5.0) + 0.916) < 1e-3
    old = set_arc(6.0)
    assert abs(tk.S2 - (10 + 3 * np.pi)) < 1e-12
    set_arc(old)
    print("ok")
