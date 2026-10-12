"""More derivative gain kd moves the Nyquist curve of the PD heading loop away from -1, but raises the gain from sensor
noise to motor torque. kd goes 0.04, 0.06, 0.08 (our loop), 0.12, 0.16, 0.2, 0.3, 0.4, kp = 0.4. Top: the
Nyquist curve and the circle round -1 of radius equal to its closest distance s_m. Bottom left: |S| in dB, peak
Ms = 1/s_m. Bottom right: the noise gain |CS| (N m of torque per rad of heading noise), 8.0 at 100 rad/s for kd = 0.08
and 40 for kd = 0.4. Grey: our loop, kd = 0.08. Run: python kd_anim.py -> kd_anim.gif, kd_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from loopkit import KP, C_pd, L_head, db, sens_peak
from shapekit import gang_of_four

here = Path(__file__).parent
kds = [0.04, 0.06, 0.08, 0.12, 0.16, 0.2, 0.3, 0.4]
wn = np.logspace(np.log10(1.0), np.log10(40), 800)
ws = np.logspace(-1, np.log10(300), 1200)
ang = np.linspace(0, 2 * np.pi, 200)
expect = {0.04: (5.03, 4.0), 0.08: (2.55, 8.0), 0.16: (1.36, 16.0), 0.2: (1.15, 20.0), 0.4: (1.0, 40.0)}


def stats(kd):
    L = lambda s: L_head(s, kd=kd)
    w, d, Ms = sens_peak(L)
    if Ms < 1.0:                       # the closest point is the origin, reached only as w -> infinity
        d, Ms = 1.0, 1.0
    noise = abs(gang_of_four(lambda s: C_pd(s, KP, kd), np.array([100.0]))["CS"][0])
    return d, Ms, noise


for kd, (ms, nz) in expect.items():
    d, Ms, noise = stats(kd)
    assert abs(Ms - ms) < 5e-3 and abs(noise - nz) < 0.05, (kd, Ms, noise)


def frame(kd, last=False):
    d, Ms, noise = stats(kd)
    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None], [{}, {}]], row_heights=[0.52, 0.48],
                        vertical_spacing=0.15, horizontal_spacing=0.15)
    for k, col, wd, name in ((0.08, GREY, 3, "our loop, Kd = 0.08"), (kd, BLUE, 5, f"Kd = {kd:g}")):
        if k == kd and k == 0.08 and col == GREY:
            continue
        Lc = L_head(1j * wn, kd=k)
        g = gang_of_four(lambda s: C_pd(s, KP, k), ws)
        fig.add_trace(go.Scatter(x=Lc.real, y=Lc.imag, mode="lines", line=dict(color=col, width=wd), name=name), 1, 1)
        fig.add_trace(go.Scatter(x=ws, y=db(g["S"]), mode="lines", line=dict(color=col, width=wd), showlegend=False),
                      2, 1)
        fig.add_trace(go.Scatter(x=ws, y=np.abs(g["CS"]), mode="lines", line=dict(color=col, width=wd),
                                 showlegend=False), 2, 2)
    fig.add_trace(go.Scatter(x=-1 + d * np.cos(ang), y=d * np.sin(ang), mode="lines",
                             line=dict(color=RED, width=2, dash="dot"), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="x"),
                             name="−1"), 1, 1)
    fig.add_trace(go.Scatter(x=[100], y=[noise], mode="markers", marker=dict(color=RED, size=13), showlegend=False),
                  2, 2)
    fig.add_annotation(x=2, y=np.log10(noise), text=f"{noise:.1f} at 100 rad/s", ax=-95, ay=-30,
                       font=dict(size=18, color=RED), arrowcolor=RED, row=2, col=2)
    fig.update_xaxes(title_text="real part", range=[-3.0, 0.6], row=1, col=1)
    fig.update_yaxes(title_text="imaginary part", range=[-1.3, 1.1], scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(type="log", range=[-1, np.log10(30)], title_text="ω (rad/s)", row=2, col=1)
    fig.update_yaxes(title_text="|S| (dB)", range=[-30, 16], row=2, col=1)
    fig.update_xaxes(type="log", range=[-1, np.log10(300)], title_text="ω (rad/s)", row=2, col=2)
    fig.update_yaxes(type="log", title_text="noise gain |CS| (N·m/rad)", range=[-2, 2], row=2, col=2)
    tag = " (our loop)" if kd == 0.08 else ""
    title = (f"Kd = {kd:g}{tag}: closest distance {d:.3f}, Ms = {Ms:.2f}<br>"
             f"noise gain at 100 rad/s: {noise:.1f} N·m/rad")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, margin=dict(l=100, r=30, t=170, b=70),
                      legend=dict(x=0.0, y=1.0, yanchor="bottom", orientation="h", font=dict(size=17)),
                      title=dict(x=0.5, y=0.975, text=title))
    return fig


figs = [frame(k) for k in kds]
make_gif(figs, here / "kd_anim", fps=1, holds=[3, 1, 3, 1, 1, 1, 1, 10], keys=[2, 7], cols=2, width=800)
