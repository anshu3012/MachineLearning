"""The guess-score-update loop on the six points (Plotly frames -> GIF). Each round has two frames: E-step (score: the
points are coloured by their shares of curves A and B) and M-step (update: the curves move to fit the shares). Right
panel: the log-likelihood after each M-step; it only goes up. Own design, own data (six_points.py)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import make_gif
from six_points import COLS, FONT, X, e_step, loglik, run, weighted

here = Path(__file__).parent
H = run(8)
RGB = np.array([[76, 120, 168], [245, 133, 24]])
g = np.linspace(-1, 11, 300)


def blend(r):
    return [f"rgb({int(a)},{int(b)},{int(c)})" for a, b, c in r @ RGB]


def frame(it, phase, colour_it=None):
    """it: iteration index of the curves shown; phase 'E' = points coloured by this iteration's curves."""
    pi, mu, var, _ = H[it]
    r = e_step(*H[it if colour_it is None else colour_it][:3])
    fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.1,
                        subplot_titles=["curves and points", "log-likelihood"])
    fig.update_annotations(font_size=22)
    w = weighted(g, pi, mu, var)
    for k in range(2):
        fig.add_trace(go.Scatter(x=g, y=w[:, k], mode="lines", line=dict(color=COLS[k], width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=X, y=np.full(6, 0.016), mode="markers",
                             marker=dict(size=26, color=blend(r), line=dict(color="black", width=2))), 1, 1)
    n = it + (1 if phase == "M" else 0)
    shown = [H[i][3] for i in range(n + 1)] if phase == "M" else [H[i][3] for i in range(it + 1)]
    fig.add_trace(go.Scatter(x=list(range(len(shown))), y=shown, mode="lines+markers",
                             line=dict(color="black", width=3), marker=dict(size=10)), 1, 2)
    fig.update_xaxes(range=[-1, 11], title="x", row=1, col=1)
    fig.update_yaxes(range=[0, 0.28], showticklabels=False, row=1, col=1)
    fig.update_xaxes(range=[-0.3, 8.3], title="iteration", dtick=1, row=1, col=2)
    fig.update_yaxes(range=[-16.5, -11], row=1, col=2)
    title = {"start": "start: a poor guess", "E": f"round {it + 1}: E-step, score every point (colour = shares)",
             "M": f"round {it}: M-step, move the curves to fit the shares"}
    return fig, title


def build():
    figs, holds = [], []
    seq = [("start", 0)]
    for it in range(0, 5):
        seq += [("E", it), ("M", it + 1)]
    seq.append(("E", 7))
    for ph, it in seq:
        if ph == "start":
            fig, t = frame(0, "E"); fig.update_layout(title_text="start: a poor guess, two curves on the left")
        elif ph == "E":
            fig, t = frame(it, "E"); fig.update_layout(title_text=t["E"] if it < 7 else "converged: nothing moves any more")
        else:
            fig, t = frame(it, "E", it - 1)   # curves after the M-step, points not yet recoloured
            fig.update_layout(title_text=f"round {it}: M-step, curves move to fit the shares")
        fig.update_layout(template="simple_white", width=1150, height=520, font=FONT, showlegend=False,
                          title=dict(x=0.5, font=dict(size=24)), margin=dict(l=60, r=30, t=100, b=60))
        figs.append(fig)
        holds.append(2)
    holds[-1] = 5
    return figs, holds


if __name__ == "__main__":
    figs, holds = build()
    make_gif(figs, here / "em_six", fps=1, holds=holds, keys=[0, 2, 4, 8, 10, len(figs) - 1], cols=2)
