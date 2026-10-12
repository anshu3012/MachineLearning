"""Figure: the robot carrying a round tray 0.8 m across (radius 0.4 m): its obstacle region (orange) leaves narrow
passages, 0.2 m under the table and about 0.1 m beside it. One run (seed 5001) of 50 milestones by each sampling
strategy, 10 nearest neighbours, trip dock to cabinet; each piece of the roadmap has its own colour. Uniform: 2
pieces (45 and 5 milestones), no route. Gaussian sampling (sigma 0.1 m): 1 piece, route 4.993 m. Bridge test (sigma
0.3 m): route 7.773 m. Run -> strategies.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import cspace as c
import drawkit as dk
import prm
import prmdraw as pd
from gifkit import FONT, GREEN, ORANGE, PURPLE

here = Path(__file__).parent
RUNS = [("uniform", 0, "uniform sampling: 2 pieces, no route", (2, None)),
        ("gaussian", 0.1, "Gaussian sampling (sigma 0.1 m): one piece, route 4.993 m", (1, 4.993)),
        ("bridge", 0.3, "bridge test (sigma 0.3 m): route 7.773 m", (2, 7.773))]
fig = make_subplots(rows=3, cols=1, vertical_spacing=0.07, subplot_titles=[r[2] for r in RUNS])
for row, (strategy, sigma, title, (pieces, length)) in enumerate(RUNS, start=1):
    w = prm.World(0.4)
    V, draws = prm.sample_strategy(w, np.random.default_rng(5001), 50, strategy, sigma, 1.0)
    E = prm.connect(w, V, prm.K)
    nc, lab = prm.components(50, E)
    P, L, _ = prm.query(w, V, E, prm.START, prm.CABINET)
    assert nc == pieces and (P is None if length is None else round(L, 3) == length)
    fig.add_trace(dk.geom_trace(w.cobs.intersection(pd.VIEW).difference(c.obstacles()), dk.COBS_FILL, ORANGE, 1.5),
                  row=row, col=1)
    dk.room(fig, row=row, col=1)
    for k in range(nc):
        col = pd.COMP[k]
        xs, ys = [], []
        for i, j in E:
            if lab[i] == k:
                xs += [V[i][0], V[j][0], None]
                ys += [V[i][1], V[j][1], None]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=1.4)), row=row, col=1)
        Q = np.array([V[i] for i in range(50) if lab[i] == k])
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="markers", marker=dict(color=col, size=8)), row=row,
                      col=1)
    if P is not None:
        Q = np.asarray(P)
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines", line=dict(color=GREEN, width=5)), row=row, col=1)
    for q, t, pos in ((prm.START, "dock", "bottom left"), (prm.CABINET, "cabinet", "middle left")):
        dk.point(fig, q[0], q[1], PURPLE, t, pos=pos, row=row, col=1, tsize=18)
    if row == 1:
        for x, y, t in ((4.0, 0.5, "0.2 m"), (6.05, 2.5, "0.1 m"), (5.62, 1.2, "0.11 m")):
            fig.add_annotation(x=x, y=y, text=f"<b>{t}</b>", showarrow=False, font=dict(size=17, color="black"),
                               bgcolor="rgba(255,255,255,0.85)", row=row, col=1)
    fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)" if row == 3 else None, showgrid=False,
                     constrain="domain", row=row, col=1)
    fig.update_yaxes(range=[-0.2, 4.3], dtick=1, title="y (m)", showgrid=False,
                     scaleanchor="x" if row == 1 else f"x{row}", row=row, col=1)
fig.update_layout(template="simple_white", width=1000, height=1650, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(selector=dict(xref="paper"), font=dict(size=21))
fig.write_image(here / "strategies.png")
