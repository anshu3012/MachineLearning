"""The opening problem: RO-070's line rule (red; turn rate -0.5 e - 2 th_e at the nearest course point, run with
RO-070's own kit, linekit.py) against pure pursuit with a 4 m look-ahead (blue), both from 1.0 m left of the course
at 2 m/s; one frame per 0.5 s. The line rule turns only in proportion to its errors, so on the arc it runs up to
0.39 m outside; pure pursuit sees the bend coming: 0.12 m inside at the entry, 0.03 m in the middle of the arc.
Run: python opening_anim.py -> opening_anim.gif, opening_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import linekit as lk
import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
line = lk.run(lambda q, t: lk.line_rule(q))
pp = tk.simulate(tk.law("pp", ld=4.0), v=tk.V_BASE)
m_pp = tk.metrics(pp)
on_arc = (line["s"] >= lk.L1) & (line["s"] <= lk.L1 + lk.L_ARC)
reach_line = line["s"][np.argmax(np.abs(line["e"]) < 0.1)]
assert abs(reach_line - 7.70) < 0.005 and abs(line["e"][on_arc].min() + 0.388) < 1e-3
assert abs(m_pp["reach"] - 7.36) < 0.01 and abs(m_pp["arc_peak"] - 0.120) < 1e-3 and abs(m_pp["arc_mid"] - 0.033) < 1e-3
RUNS = ((line, RED, f"line rule: within 0.1 m after {reach_line:.1f} m; on the arc up to "
                    f"{-line['e'][on_arc].min():.2f} m outside"),
        (pp, BLUE, f"pure pursuit, 4 m: within 0.1 m after {m_pp['reach']:.1f} m; on the arc "
                   f"{m_pp['arc_peak']:.2f} m inside, then {m_pp['arc_mid']:.2f} m"))


def frame(t, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.66, 0.34], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    for r, c, lab in RUNS:
        i = min(int(round(t / tk.DT)), len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["x"][:i + 1], y=r["y"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=1, col=1)
        for tr in car_traces(r["x"][i], r["y"][i], r["th"][i], r["delta"][i], c):
            fig.add_trace(tr, row=1, col=1)
        fig.add_trace(go.Scatter(x=r["s"][:i + 1], y=r["e"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 name=lab if last else lab.split(":")[0]), row=2, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=0.95, text="arc", showarrow=False, font=dict(size=18, color=GREY),
                       row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    sub = "the whole course" if last else f"t = {t:.1f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top",
                                 text=f"the line rule (red) and pure pursuit (blue), 2 m/s<br>{small}{sub}</span>"),
                      legend=dict(x=0.01, y=0.985, font=dict(size=16), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 24], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.5, 1.05], dtick=0.25, row=2, col=1)
    return fig


t_end = max(line["t"][-1], pp["t"][-1])
ts = list(np.round(np.arange(0, t_end, 0.5), 2)) + [t_end]
figs = [frame(t) for t in ts] + [frame(t_end, last=True)]
n = len(figs)
make_gif(figs, here / "opening_anim", fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, 8, 20, n - 1], cols=2,
         width=850)
