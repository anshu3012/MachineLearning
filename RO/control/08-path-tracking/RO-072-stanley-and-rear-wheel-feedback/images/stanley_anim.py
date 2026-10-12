"""Stanley from 1.0 m left of the course at 2 m/s (top) and 5 m/s (middle), one frame per 0.1 s for 3 s.
At each front axle two arrows: purple, the course's direction at the nearest point (where the heading term alone
would point the wheel); orange, the wheel's commanded direction, turned further towards the course by the
cross-track term. Bottom: the front axle's lateral error against time, with the straight-line prediction
exp(-k v t / (ks + v)) dashed. The error halves in 1.03 s at 2 m/s and 0.81 s at 5 m/s, though the faster car drives
4.0 m in that time against 2.0 m.
Run: python stanley_anim.py -> stanley_anim.gif, stanley_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
SPEEDS, COLS = (2.0, 5.0), (BLUE, "#2E8B57")
runs = [tk.simulate(tk.law("stanley"), v=v) for v in SPEEDS]
half = [r["t"][np.argmax(np.abs(r["ef"]) < 0.5)] for r in runs]
assert abs(half[0] - 1.03) < 0.005 and abs(half[1] - 0.81) < 0.005
ARROW = 2.5   # m, drawn arrow length
T_END = 3.0


def ax_name(row):
    return "" if row == 1 else str(row)


def arrow(fig, x0, y0, ang, color, row):
    a = ax_name(row)
    fig.add_annotation(x=x0 + ARROW * np.cos(ang), y=y0 + ARROW * np.sin(ang), ax=x0, ay=y0, xref=f"x{a}",
                       yref=f"y{a}", axref=f"x{a}", ayref=f"y{a}", showarrow=True, arrowhead=2, arrowsize=1.3,
                       arrowwidth=3, arrowcolor=color)


def frame(t, last=False):
    fig = make_subplots(rows=3, cols=1, row_heights=[0.25, 0.25, 0.5], vertical_spacing=0.08,
                        subplot_titles=["2 m/s", "5 m/s", ""])
    for row, (v, r, c) in enumerate(zip(SPEEDS, runs, COLS), start=1):
        i = int(round(t / tk.DT))
        k = min(int(t * tk.RATE + 1e-9), len(r["ticks"]) - 1)
        tick = r["ticks"][k]
        fig.add_trace(course_trace(s_to=20), row=row, col=1)
        fig.add_trace(go.Scatter(x=r["x"][:i + 1], y=r["y"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=row, col=1)
        for tr in car_traces(r["x"][i], r["y"][i], r["th"][i], r["delta"][i], c):
            fig.add_trace(tr, row=row, col=1)
        if not last:
            th_path = tick["th"] - tick["the"]
            arrow(fig, tick["fx"], tick["fy"], th_path, PURPLE, row)
            arrow(fig, tick["fx"], tick["fy"], tick["th"] + tick["delta_cmd"], ORANGE, row)
            head_deg = np.degrees(tick["head"])
            head_txt = f"{head_deg:+.1f}" if abs(head_deg) >= 0.05 else "+0.0"
            fig.add_annotation(x=-0.6, y=3.3, xref=f"x{ax_name(row)}", yref=f"y{ax_name(row)}", showarrow=False,
                               xanchor="left", font=dict(size=17),
                               text=(f"<span style='color:{PURPLE}'>heading term {head_txt}°</span>, "
                                     f"<span style='color:{ORANGE}'>cross-track term "
                                     f"{np.degrees(tick['cross']):+.1f}°</span>"))
        fig.update_xaxes(range=[-1, 18], dtick=5, row=row, col=1)
        fig.update_yaxes(title_text="y (m)", range=[-1.3, 4.0], dtick=1, scaleanchor=f"x{ax_name(row)}", scaleratio=1,
                         row=row, col=1)
        tt = r["t"][:i + 1]
        fig.add_trace(go.Scatter(x=tt, y=r["ef"][:i + 1], mode="lines", line=dict(color=c, width=4),
                                 name=f"{v:.0f} m/s: halves in {half[row - 1]:.2f} s"), row=3, col=1)
        rate = tk.K_ST * v / (tk.KS_ST + v)
        tp = np.linspace(0, T_END, 200)
        fig.add_trace(go.Scatter(x=tp, y=np.exp(-rate * tp), mode="lines", line=dict(color=c, width=2, dash="dash"),
                                 name=f"{v:.0f} m/s: exp(−{rate:.3f} t)"), row=3, col=1)
    fig.add_vline(x=t, line=dict(color=GREY, width=1.5, dash="dot"), row=3, col=1)
    fig.add_hline(y=0.5, line=dict(color=GREY, width=1, dash="dot"), row=3, col=1)
    small = "<span style='font-size:19px'>"
    sub = "the first 3 s" if last else f"t = {t:.1f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1200, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.98, yanchor="top",
                                 text=f"Stanley from 1.0 m off, at 2 and 5 m/s<br>{small}{sub}</span>"),
                      legend=dict(x=0.55, y=0.40, font=dict(size=17), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="time (s)", range=[0, T_END], dtick=0.5, row=3, col=1)
    fig.update_yaxes(title_text="front-axle lateral error (m)", range=[0, 1.05], dtick=0.25, row=3, col=1)
    return fig


ts = list(np.round(np.arange(0, T_END + 1e-9, 0.1), 2))
figs = [frame(t) for t in ts] + [frame(T_END, last=True)]
n = len(figs)
make_gif(figs, here / "stanley_anim", fps=5, holds=[8] + [1] * (n - 2) + [20], keys=[0, 5, 10, n - 1], cols=2,
         width=850)
