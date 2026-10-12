"""Reversing: the car faces along the first straight, 1.0 m left of it, and drives backwards at 2 m/s for 8 s;
one frame per 0.25 s. Orange: Stanley, which steers from its front axle; in reverse that axle trails, and the car
swings round until it faces the other way, 9.0 m to the right of the line. Blue: rear-wheel feedback, whose law
holds for either direction of travel: it returns within 0.1 m after 2.1 s (4.1 m driven back), 0.04 m past the line.
Run: python reverse_anim.py -> reverse_anim.gif, reverse_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
START_REV = (8.0, 1.0, 0.0)
runs = {name: tk.simulate(tk.law(name), v=-2.0, start=START_REV, s_stop=1e9, t_max=8.0) for name in ("stanley", "rear")}
st, rw = runs["stanley"], runs["rear"]
i_rw = np.argmax(np.abs(rw["e"]) < 0.1)
assert abs(rw["t"][i_rw] - 2.1) < 0.01 and abs(-rw["e"].min() - 0.039) < 1e-3
assert np.degrees(abs(st["th"]).max()) > 170 and abs(st["e"][-1] + 9.0) < 0.01
X0, X1 = min(st["x"].min(), rw["x"].min()) - 3, 11
Y0, Y1 = min(st["y"].min(), rw["y"].min()) - 3, 4


def frame(t, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.62, 0.38], vertical_spacing=0.09)
    fig.add_trace(go.Scatter(x=[X0, X1], y=[0, 0], mode="lines", line=dict(color="#BBBBBB", width=6), showlegend=False),
                  row=1, col=1)
    i = min(int(round(t / tk.DT)), len(st["t"]) - 1)
    for r, c, name in ((st, ORANGE, "Stanley (front axle)"), (rw, BLUE, "rear-wheel feedback (rear axle)")):
        fig.add_trace(go.Scatter(x=r["x"][:i + 1], y=r["y"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=1, col=1)
        for tr in car_traces(r["x"][i], r["y"][i], r["th"][i], r["delta"][i], c):
            fig.add_trace(tr, row=1, col=1)
        fig.add_trace(go.Scatter(x=r["t"][:i + 1], y=r["e"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 name=name), row=2, col=1)
    fig.add_annotation(x=X1 - 0.5, y=2.8, text="driving backwards, 2 m/s", showarrow=False, xanchor="right",
                       font=dict(size=18, color=GREY), row=1, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    if last:
        sub = (f"8 s: Stanley faces the other way, {abs(st['e'][-1]):.1f} m to the right; rear-wheel feedback "
               f"within 0.1 m after {rw['t'][i_rw]:.1f} s")
    else:
        sub = f"t = {t:.2f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1100, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=f"reversing from 1.0 m off<br>{small}{sub}</span>"),
                      legend=dict(x=0.02, y=0.03, yanchor="bottom", font=dict(size=18), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[X0, X1], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[Y0, Y1], dtick=2, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="time (s)", range=[0, 8], dtick=1, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-9.5, 1.2], dtick=1, row=2, col=1)
    return fig


ts = list(np.round(np.arange(0, 8.0, 0.25), 2)) + [8.0]
figs = [frame(t) for t in ts] + [frame(8.0, last=True)]
n = len(figs)
make_gif(figs, here / "reverse_anim", fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, 8, 16, n - 1], cols=2,
         width=850)
