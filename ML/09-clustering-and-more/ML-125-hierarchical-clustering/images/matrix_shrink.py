"""The proximity matrix shrinking merge by merge with single linkage (Plotly frames -> GIF), on the five points of
section 7: P1 = (1, 1), P2 = (2, 2), P3 = (5, 4), P4 = (6, 4), P5 = (6, 6). Left: the points, one colour per cluster.
Right: the current matrix, the smallest off-diagonal entry outlined in red; that pair merges and its two rows and
columns become one. Merges at 1.00, 1.41, 2.00 and 3.61, as in section 8.1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial.distance import cdist
from gifkit import FONT, RED, make_gif

here = Path(__file__).parent
P = np.array([[1, 1], [2, 2], [5, 4], [6, 4], [6, 6]], float)
D0 = cdist(P, P)
COL = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#9D755D"]


def run():
    """Single linkage: list of (names, members, matrix, (i, j) to merge or None)."""
    names, members, steps, c = [f"P{i + 1}" for i in range(5)], [[i] for i in range(5)], [], 0
    while True:
        n = len(members)
        M = np.array([[0 if a == b else min(D0[i, j] for i in members[a] for j in members[b]) for b in range(n)] for a in range(n)])
        if n == 1:
            steps.append((names[:], [m[:] for m in members], M, None))
            return steps
        off = M + np.eye(n) * 1e9
        i, j = sorted(np.unravel_index(off.argmin(), off.shape))
        steps.append((names[:], [m[:] for m in members], M, (i, j)))
        c += 1
        members[i] = sorted(members[i] + members[j]); names[i] = f"C{c}"
        del members[j], names[j]


STEPS = run()
assert [round(float(s[2][s[3]]), 2) for s in STEPS[:-1]] == [1.00, 1.41, 2.00, 3.61]       # the Note, section 8.1


def frame(k):
    names, members, M, pair = STEPS[k]
    n = len(names)
    title = (f"smallest distance {M[pair]:.2f}: merge {names[pair[0]]} and {names[pair[1]]}" if pair else "one cluster left: done")
    fig = make_subplots(1, 2, column_widths=[0.45, 0.55], horizontal_spacing=0.12,
                        subplot_titles=[f"{n} cluster{'s' if n > 1 else ''}", f"proximity matrix: {n} × {n}"])
    fig.update_annotations(font_size=22, yshift=28)
    for c, (nm, mem) in enumerate(zip(names, members)):
        fig.add_trace(go.Scatter(x=P[mem, 0], y=P[mem, 1], mode="markers+text", text=[f"P{i + 1}" for i in mem], textposition="top center",
                                 textfont=dict(size=20), marker=dict(size=22, color=COL[min(mem)], line=dict(color="black", width=1))), 1, 1)
    if pair:
        a, b = min(((i, j) for i in members[pair[0]] for j in members[pair[1]]), key=lambda t: D0[t])
        fig.add_trace(go.Scatter(x=P[[a, b], 0], y=P[[a, b], 1], mode="lines", line=dict(color=RED, width=5, dash="dash")), 1, 1)
    fig.add_trace(go.Heatmap(z=M, x=names, y=names, colorscale="Blues", reversescale=True, zmin=0, zmax=7.1, showscale=False,
                             text=M.round(2), texttemplate="%{text:.2f}", textfont=dict(size=20)), 1, 2)
    if pair:
        for i, j in (pair, pair[::-1]):
            fig.add_shape(type="rect", x0=j - 0.5, x1=j + 0.5, y0=i - 0.5, y1=i + 0.5, line=dict(color=RED, width=5),
                          fillcolor="rgba(0,0,0,0)", opacity=1, row=1, col=2)
    fig.update_xaxes(range=[0, 7], title="x", row=1, col=1)
    fig.update_yaxes(range=[0, 7.2], title="y", row=1, col=1)
    fig.update_yaxes(autorange="reversed", row=1, col=2)
    fig.update_xaxes(side="top", row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False, margin=dict(l=60, r=20, t=140, b=60),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=24)))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(5)], here / "matrix_shrink", fps=1, holds=[3, 3, 3, 3, 4], keys=[1, 2], cols=1)
