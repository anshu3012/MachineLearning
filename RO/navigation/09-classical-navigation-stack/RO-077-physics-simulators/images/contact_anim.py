"""The landing of the running example, one step of 0.002 s per frame from 136 ms to 200 ms, then one frame per 10 ms
to 350 ms. The height of the box's bottom is in millimetres (the floor is at 0; grey below it is inside the floor).
Top, hard contact: in the step
whose end would be inside the floor, an impulse of 1.39 N s stops the fall at once and a friction impulse of
0.56 N s takes the sideways speed from 2.00 to 1.44 m/s; the box never enters the floor. Bottom, soft contact
(a spring and a damper, MuJoCo's default time constant 0.02 s): the box sinks up to 9.7 mm, the push grows with the
depth to 140 N and pushes it back, and it settles 3.9 mm deep, where the push equals its weight, 9.81 N.
Run -> contact_anim.gif, contact_anim_frames.png"""
import numpy as np
import plotly.graph_objects as go
import simkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from plotly.subplots import make_subplots

DT = 0.002
H = s.simulate(DT, T=0.4, contact="hard")
S = s.simulate(DT, T=0.4, contact="soft")
kh = int(np.argmax(H[:, 5] > 0))
assert round(H[kh, 5] * DT, 2) == 1.39 and round(-H[kh, 6] * DT, 2) == 0.56 and round(H[kh, 3], 2) == 1.44
assert round(S[:, 7].max() * 1000, 1) == 9.7 and round(S[:, 5].max()) == 140
assert round(S[-1, 7] * 1000, 1) == 3.9
T0, T1 = 0.136, 0.350


def panel(fig, row, R, k, col, title, note):
    sel = (R[:, 0] >= T0 - 1e-9) & (np.arange(len(R)) <= k)
    fig.add_trace(go.Scatter(x=[T0 * 1000 - 1, T1 * 1000 + 1, T1 * 1000 + 1, T0 * 1000 - 1], y=[0, 0, -12, -12],
                             fill="toself", fillcolor="rgba(150,150,150,0.3)", mode="none"), row=row, col=1)
    fig.add_trace(go.Scatter(x=R[sel, 0] * 1000, y=R[sel, 2] * 1000, mode="lines+markers",
                             line=dict(color=col, width=2.5), marker=dict(size=7, color=col)), row=row, col=1)
    t, x, z, vx, vz, N, f, d = R[k]
    fig.add_annotation(x=T0 * 1000 + 1, y=19, xref=f"x{row}", yref=f"y{row}", text=f"<b>{title}</b>",
                       showarrow=False, xanchor="left", yanchor="top", font=dict(size=19, color=col))
    lines = [f"t = {t * 1000:.0f} ms: height {z * 1000:.1f} mm",
             f"floor's push {N:.1f} N, down speed {abs(vz) if abs(vz) < 5e-4 else -vz:.3f} m/s",
             f"sideways speed {vx:.3f} m/s"]
    if note:
        lines.append(note)
    fig.add_annotation(x=T1 * 1000 - 1, y=19, xref=f"x{row}", yref=f"y{row}", text="<br>".join(lines),
                       showarrow=False, xanchor="right", yanchor="top", align="right", font=dict(size=16),
                       bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=T1 * 1000 - 1, y=-11, xref=f"x{row}", yref=f"y{row}", text="inside the floor",
                       showarrow=False, xanchor="right", yanchor="bottom", font=dict(size=15, color=GREY))
    fig.update_xaxes(range=[T0 * 1000 - 1, T1 * 1000 + 1], row=row, col=1, showgrid=False,
                     title_text="time (ms)" if row == 2 else None)
    fig.update_yaxes(range=[-12, 20], row=row, col=1, showgrid=False, title_text="bottom height (mm)")


def frame(t):
    k_h = int(np.argmin(np.abs(H[:, 0] - t)))
    k_s = int(np.argmin(np.abs(S[:, 0] - t)))
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1)
    nh = ("impulse 1.39 N s stops the fall in one step;<br>friction impulse 0.56 N s: 2.00 → 1.44 m/s"
          if k_h >= kh else "")
    ns = ""
    if S[k_s, 7] > 0:
        ns = f"sunk {S[k_s, 7] * 1000:.1f} mm: push = 2500 × depth + 100 × down speed"
    panel(fig, 1, H, k_h, BLUE, "hard contact", nh)
    panel(fig, 2, S, k_s, ORANGE, "soft contact", ns)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1100, showlegend=False,
                      margin=dict(l=90, r=20, t=20, b=60))
    return fig


ts = [round(v, 3) for v in np.arange(T0, 0.2 - 1e-9, DT)] + [round(v, 3) for v in np.arange(0.2, T1 + 1e-9, 0.01)]
figs = [frame(t) for t in ts]
holds = [4] + [1] * (len(ts) - 2) + [14]
holds[ts.index(0.142)] = 6
make_gif(figs, "contact_anim", fps=4, holds=holds, keys=[ts.index(0.142), ts.index(0.164), len(ts) - 1], cols=3)
