"""Section 7: the proximity matrix of the five points P1 = (1, 1), P2 = (2, 2), P3 = (5, 4), P4 = (6, 4), P5 = (6, 6).
Left: all 5 x 5 Euclidean distances, the smallest off the diagonal (P3-P4, 1.00) outlined. Right: after the merge,
the 4 x 4 matrix; the distances between unchanged points stay, the row of C1 = {P3, P4} waits for a linkage rule.
Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial.distance import cdist

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=17)
P = np.array([[1, 1], [2, 2], [5, 4], [6, 4], [6, 6]], float)
D = cdist(P, P)
assert np.allclose(D[0].round(2), [0, 1.41, 5.00, 5.83, 7.07]) and round(D[2, 3], 2) == 1.00
names = ["P1", "P2", "P3", "P4", "P5"]
keep = [0, 1, 4]
names2 = ["P1", "P2", "C1", "P5"]
D2 = np.full((4, 4), np.nan)
idx = {0: 0, 1: 1, 3: 4}
for a, i in idx.items():
    for b, j in idx.items():
        D2[a, b] = D[i, j]
D2[2, 2] = 0
txt2 = [["?" if np.isnan(v) else f"{v:.2f}" for v in row] for row in D2]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("all 5 points: merge the closest pair", "after the merge: C1 = {P3, P4}"))
fig.add_trace(go.Heatmap(z=D, x=names, y=names, colorscale="Blues", reversescale=True, zmin=0, zmax=7.1, showscale=False,
                         text=D.round(2), texttemplate="%{text:.2f}", textfont=dict(size=18)), row=1, col=1)
fig.add_shape(type="rect", x0=2.5, x1=3.5, y0=1.5, y1=2.5, line=dict(color="#E45756", width=4), fillcolor="rgba(0,0,0,0)", opacity=1, row=1, col=1)
fig.add_shape(type="rect", x0=1.5, x1=2.5, y0=2.5, y1=3.5, line=dict(color="#E45756", width=4), fillcolor="rgba(0,0,0,0)", opacity=1, row=1, col=1)
fig.add_trace(go.Heatmap(z=np.nan_to_num(D2, nan=8), x=names2, y=names2, colorscale=[[0, "#08306b"], [0.87, "#f7fbff"], [1, "#FDE5CC"]],
                         zmin=0, zmax=8, showscale=False, text=txt2, texttemplate="%{text}", textfont=dict(size=18)), row=1, col=2)
for c in (1, 2):
    fig.update_yaxes(autorange="reversed", row=1, col=c)
    fig.update_xaxes(side="top", row=1, col=c)
fig.update_layout(template="simple_white", width=1100, height=500, font=FONT, margin=dict(l=40, r=20, t=120, b=20))
fig.update_annotations(yshift=30)
fig.write_image(here / "proximity.png", scale=2)
fig.write_image(here / "proximity.pdf")
