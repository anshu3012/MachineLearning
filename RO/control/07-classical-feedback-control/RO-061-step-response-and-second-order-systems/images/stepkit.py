"""Shared model for this Note (no output when run on its own): the robot's speed loop under P control and its heading
loop under PD control, their step responses, and the four numbers read off a step response.

Speed plant:   m dv/dt = u - b v,       m = 8 kg, b = 2 N s/m, u = Kp (v_ref - v), |u| <= 4 N.
Heading plant: I dw/dt = tau, dth/dt = w, I = 0.1 kg m^2,     tau = Kp (th_ref - th) - Kd w, |tau| <= 0.2 N m.
"""
import numpy as np

M, B, I = 8.0, 2.0, 0.1                 # mass (kg), rolling drag (N s/m), yaw inertia (kg m^2)
F_MAX, TAU_MAX = 4.0, 0.2               # drive force limit (N), turning torque limit (N m)
V_REF, TH_REF = 0.5, 0.5                # speed step (m/s), heading step (rad)
KP_V = 6.0                              # P gain of the speed loop (N per m/s)
KP_TH, KD_OLD, KD_NEW = 0.4, 0.08, 0.4  # PD gains of the heading loop (N m/rad, N m s/rad): first try and the fix


def speed_p(t, kp=KP_V, v_ref=V_REF):
    """Speed under P control from rest: first order, time constant m/(kp + b), final value kp/(kp + b) v_ref."""
    tau = M / (kp + B)
    return kp / (kp + B) * v_ref * (1 - np.exp(-t / tau))


def wn_zeta(kp=KP_TH, kd=KD_NEW):
    """Natural frequency and damping ratio of I e'' + kd e' + kp e = 0."""
    return np.sqrt(kp / I), kd / (2 * np.sqrt(kp * I))


def second_order(t, wn, zeta, step=TH_REF):
    """Step response of wn^2 / (s^2 + 2 zeta wn s + wn^2) from rest (FBS eq. 7.24)."""
    t = np.asarray(t, dtype=float)
    if abs(zeta - 1) < 1e-9:
        return step * (1 - np.exp(-wn * t) * (1 + wn * t))
    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta ** 2)
        return step * (1 - np.exp(-zeta * wn * t) * (np.cos(wd * t) + zeta / np.sqrt(1 - zeta ** 2) * np.sin(wd * t)))
    r = np.sqrt(zeta ** 2 - 1)
    s1, s2 = -wn * (zeta - r), -wn * (zeta + r)
    return step * (1 + (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s1 - s2))


def heading_pd(t, kp=KP_TH, kd=KD_NEW, step=TH_REF):
    """Heading and turn rate under PD (derivative on the measured turn rate), and the torque it commands."""
    wn, z = wn_zeta(kp, kd)
    th = second_order(t, wn, z, step)
    w = np.gradient(th, t)
    return th, w, kp * (step - th) - kd * w


def roots(wn, zeta):
    """The two roots of s^2 + 2 zeta wn s + wn^2 = 0 (complex numbers)."""
    return np.roots([1, 2 * zeta * wn, wn ** 2]).astype(complex)


def _cross(t, y, level):
    i = int(np.argmax(y >= level))
    return t[i - 1] + (level - y[i - 1]) * (t[i] - t[i - 1]) / (y[i] - y[i - 1])


def step_info(t, y, final, ref, band=0.02):
    """The four numbers of a step response that starts at 0: rise time (10 to 90 percent of the final value),
    overshoot (fraction of the final value), settling time (stays within 2 percent), steady-state error."""
    ip = int(np.argmax(y))
    out = np.where(np.abs(y - final) > band * abs(final))[0]
    return dict(rise=_cross(t, y, 0.9 * final) - _cross(t, y, 0.1 * final), t10=_cross(t, y, 0.1 * final),
                t90=_cross(t, y, 0.9 * final), overshoot=max(0.0, (y[ip] - final) / final), peak=y[ip], t_peak=t[ip],
                settle=(t[out[-1] + 1] if out[-1] + 1 < len(t) else np.inf) if len(out) else 0.0,
                sse=ref - final)


if __name__ == "__main__":
    t = np.linspace(0, 20, 200001)
    s = step_info(t, speed_p(t), 0.375, V_REF)
    assert abs(s["rise"] - 2.197) < 1e-3 and abs(s["settle"] - 3.912) < 1e-3 and abs(s["sse"] - 0.125) < 1e-12
    th, _, tq = heading_pd(t, kd=KD_OLD)
    h = step_info(t, th, TH_REF, TH_REF)
    assert abs(h["overshoot"] - 0.5266) < 1e-4 and abs(h["peak"] - 0.7633) < 1e-4 and abs(h["settle"] - 9.80) < 0.01
    th, _, tq = heading_pd(t)
    h = step_info(t, th, TH_REF, TH_REF)
    assert h["overshoot"] == 0 and abs(h["settle"] - 2.917) < 1e-3 and abs(h["rise"] - 1.679) < 1e-3
    assert tq.max() <= TAU_MAX + 1e-9 and tq.min() > -TAU_MAX
