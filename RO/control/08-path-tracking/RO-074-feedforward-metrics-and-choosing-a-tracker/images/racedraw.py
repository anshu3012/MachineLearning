"""The four trackers raced on the test course, for race.py and race_fast.py (no output when run on its own).
Every car starts on the line (rear axle at (0, 0), heading 0), so every error comes from the curve and the speed.
Lateral error and metrics at the rear axle for every tracker (ffkit.scores)."""
from functools import partial

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import ffkit as fk
import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

ON_LINE = (0.0, 0.0, 0.0)
TRACKERS = [("pure pursuit", tk.law("pp"), BLUE), ("Stanley", tk.law("stanley"), ORANGE),
            ("rear-wheel feedback", tk.law("rear"), GREEN),
            ("line rule + curve's turn", partial(fk.line_rule, ff=True), PURPLE)]


def race(v, tau=0.0):
    runs = [tk.simulate(f, v=v, start=ON_LINE, tau=tau) for _, f, _ in TRACKERS]
    return runs, [fk.scores(r) for r in runs]


def make(runs, sc, out, title, ylim_e, ylim_d, every=0.5):
    n = max(len(r["t"]) for r in runs)
    step = int(round(every / tk.DT))
    idx = list(range(0, n, step)) + [n - 1]

    def frame(i, last):
        fig = make_subplots(rows=4, cols=1, row_heights=[0.36, 0.25, 0.2, 0.19], vertical_spacing=0.055,
                            specs=[[{"type": "xy"}], [{"type": "xy"}], [{"type": "xy"}], [{"type": "table"}]])
        fig.add_trace(course_trace(), row=1, col=1)
        for (name, _, col), r, m in zip(TRACKERS, runs, sc):
            k = min(i, len(r["t"]) - 1)
            fig.add_trace(go.Scatter(x=r["x"][:k + 1], y=r["y"][:k + 1], mode="lines",
                                     line=dict(color=col, width=2, simplify=False), showlegend=False), row=1, col=1)
            for t in car_traces(r["x"][k], r["y"][k], r["th"][k], r["delta"][k], col, body=False):
                fig.add_trace(t, row=1, col=1)
            lab = name
            fig.add_trace(go.Scatter(x=r["s"][:k + 1], y=r["e"][:k + 1], mode="lines",
                                     line=dict(color=col, width=4, simplify=False), name=lab), row=2, col=1)
            fig.add_trace(go.Scatter(x=r["s"][:k + 1], y=np.degrees(r["delta"][:k + 1]), mode="lines",
                                     line=dict(color=col, width=3, simplify=False), showlegend=False), row=3, col=1)
        cells = [[n for n, _, _ in TRACKERS]] + ([[f"{m[q]:.3f}" for m in sc] for q in ("rms", "peak")]
                                                 + [[f"{m['travel']:.0f}" for m in sc]] if last else [["…"] * 4] * 3)
        fig.add_trace(go.Table(header=dict(values=["tracker", "RMS error (m)", "peak error (m)", "steering travel (°)"],
                                           font=dict(size=17), align="left", height=30,
                                           fill_color="#EEEEEE"),
                               cells=dict(values=cells, font=dict(size=17, color=[[c for _, _, c in TRACKERS]] * 4),
                                          align="left", height=29), columnwidth=[2.3, 1.2, 1.2, 1.5]), row=4, col=1)
        for row in (2, 3):
            for s0 in (tk.S1, tk.S2):
                fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=row, col=1, exclude_empty_subplots=False)
        fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=ylim_e[1], yanchor="top", text="arc", showarrow=False,
                           font=dict(size=18, color=GREY), row=2, col=1)
        fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1, exclude_empty_subplots=False)
        t_now = runs[0]["t"][min(i, len(runs[0]["t"]) - 1)]
        small = "<span style='font-size:19px'>"
        sub = "the run has ended: metrics at the rear axle in the table" if last else f"t = {t_now:.1f} s; metrics when the run ends"
        fig.update_layout(template="simple_white", font=FONT, width=1000, height=1600,
                          margin=dict(l=100, r=30, t=135, b=70),
                          title=dict(x=0.5, y=0.982, yanchor="top", text=f"{title}<br>{small}{sub}</span>"),
                          legend=dict(x=0.62, y=0.97, font=dict(size=17), bgcolor="rgba(255,255,255,0.88)"))
        fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, constrain="domain", constraintoward="left", row=1, col=1)
        fig.update_yaxes(title_text="y (m)", range=[-2, 23], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
        fig.update_xaxes(range=[0, 36.5], dtick=5, row=2, col=1)
        fig.update_yaxes(title_text="lateral error (m)<br>+ = left", range=ylim_e, row=2, col=1)
        fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=3, col=1)
        fig.update_yaxes(title_text="steering (°)", range=ylim_d, row=3, col=1)
        return fig

    figs = [frame(i, False) for i in idx] + [frame(idx[-1], True)]
    mid = int(np.argmin(np.abs(np.array([runs[0]["s"][min(i, len(runs[0]["s"]) - 1)] for i in idx]) - tk.S_MID)))
    make_gif(figs, out, fps=4, holds=[6] + [1] * (len(idx) - 1) + [18], keys=[0, mid, len(figs) - 2, len(figs) - 1],
             cols=2, width=850)
