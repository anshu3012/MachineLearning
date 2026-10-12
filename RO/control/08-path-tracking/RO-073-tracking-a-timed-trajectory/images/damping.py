"""Three heading gains on the same start, one frame per 0.25 s for the first 8 s: the sideways error y_e of Kanayama's
tracker for damping ratio 0.5 (K_th = 4 per m), 1 (8 per m, this Note's choice) and 2 (16 per m), with K_y = 16 per m^2,
K_x = 1 per s, v_r = 0.3 m/s. Damping 0.5 swings 1.1 cm past the line; damping 1 stays within 1 cm from 3.07 s without
crossing it by more than 0.06 cm; damping 2 creeps and stays within 1 cm only from 6.17 s.
Run: python damping.py -> damping.gif, damping_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, PURPLE, make_gif
from trackkit import DT, errors, kanayama, simulate

here = Path(__file__).parent
cases = [(4.0, 0.5, ORANGE), (8.0, 1.0, BLUE), (16.0, 2.0, PURPLE)]
ys = {}
for kth, zeta, _ in cases:
    r = simulate(lambda t, p, kth=kth: kanayama(t, p, kth=kth))
    assert not r["clipped"]
    ys[zeta] = 100 * errors(r)[1]
t = r["t"]


def settle(y):
    """First time after which |y| stays below 1 cm."""
    bad = np.where(np.abs(y) >= 1.0)[0]
    return t[bad[-1] + 1]


st = {z: settle(y) for z, y in ys.items()}
assert abs(ys[0.5].max() - 1.07) < 0.005 and ys[1.0].max() < 0.07 and ys[2.0].max() < 0
assert abs(st[0.5] - 3.31) < 1e-9 and abs(st[1.0] - 3.07) < 1e-9 and abs(st[2.0] - 6.17) < 1e-9

steps = [int(round(s / DT)) for s in np.arange(0, 8.01, 0.25)]


def frame(k):
    fig = go.Figure()
    fig.add_hrect(y0=-1, y1=1, fillcolor="#DDDDDD", opacity=0.5, line_width=0, layer="below")
    for kth, zeta, col in cases:
        y = ys[zeta]
        lab = f"damping ratio {zeta:g} (K<sub>θ</sub> = {kth:g} per m)"
        if t[k] >= st[zeta]:
            lab += f": within 1 cm from {st[zeta]:.2f} s"
        fig.add_trace(go.Scatter(x=t[:k + 1], y=y[:k + 1], mode="lines", line=dict(color=col, width=5), name=lab))
        fig.add_trace(go.Scatter(x=[t[k]], y=[y[k]], mode="markers", marker=dict(color=col, size=13), showlegend=False))
    fig.add_annotation(x=7.9, y=1.0, text="within 1 cm", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(size=18, color="#777777"))
    title = (f"t = {t[k]:.2f} s: sideways error y<sub>e</sub> for three heading gains<br><span style='font-size:19px'>"
             "same start (0.1 m left of the timetable), same K<sub>y</sub> = 16 per m², K<sub>x</sub> = 1 per s</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=760, margin=dict(l=100, r=30, t=130, b=70),
                      title=dict(text=title, x=0.5, y=0.96, yanchor="top"),
                      legend=dict(x=0.4, y=0.3, font=dict(size=19), bgcolor="rgba(255,255,255,0.85)"),
                      xaxis=dict(range=[0, 8], title="time (s)"),
                      yaxis=dict(range=[-10.5, 2.5], title="y<sub>e</sub> (cm)", dtick=2))
    return fig


figs = [frame(k) for k in steps]
make_gif(figs, here / "damping", fps=5, holds=[8] + [1] * (len(steps) - 2) + [16],
         keys=[0, 8, 14, len(steps) - 1], cols=2, width=800)
