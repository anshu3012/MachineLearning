"""From cells to the exponential curve. The 3 m of beam in front of the wall is cut into cells of length Delta; each
cell is blocked with chance b = lambda Delta, lambda = 2 per m, so the blocking chance per metre stays fixed. The
bar of cell j is P(first stop at cell j) = (1 - b)^(j - 1) b divided by Delta (share per metre, so its area is the
chance). As Delta shrinks from 0.1 m to 0.001 m the bars rise onto lambda e^(-lambda z) = 2 e^(-2z); the cell that
starts at 1 m gives 0.215, 0.265, 0.270 per m against the curve's 0.271 (the Note's table). Run -> shrink_cells.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from roomkit import text

here = Path(__file__).parent
LAM, WALL = 2.0, 3.0
DELTAS = [0.1, 0.05, 0.02, 0.01, 0.005, 0.001]
Z = np.linspace(0, WALL, 1201)
ZOOM = (0.8, 1.3, 0.42)                                    # zoom box: x from, x to, y top


def bars(d):
    n = round(WALL / d)
    j = np.arange(1, n + 1)
    b = LAM * d
    return (j - 0.5) * d, (1 - b) ** (j - 1) * b / d, round(1 / d)   # centres, heights, index of the cell from 1 m


def at1(d):
    return bars(d)[1][round(1 / d)]


def frame(d):
    x, h, i1 = bars(d)
    b = LAM * d
    fig = go.Figure()
    for xa, ya, px in (("x", "y", 450 / 3.05), ("x2", "y2", 460 / 0.5)):
        edge = dict(color="white", width=1) if d * px >= 6 else dict(width=0)
        fig.add_trace(go.Bar(x=x, y=h, width=d, marker=dict(color=ORANGE, line=edge), xaxis=xa, yaxis=ya))
        fig.add_trace(go.Bar(x=[x[i1]], y=[h[i1]], width=d, marker=dict(color=RED, line=edge), xaxis=xa, yaxis=ya))
        fig.add_trace(go.Scatter(x=Z, y=LAM * np.exp(-LAM * Z), mode="lines", line=dict(color=BLUE, width=3),
                                 xaxis=xa, yaxis=ya))
    fig.add_trace(go.Scatter(x=[x[i1]], y=[h[i1]], mode="markers", marker=dict(color=RED, size=21), xaxis="x2", yaxis="y2"))
    fig.add_trace(go.Scatter(x=[1.0], y=[LAM * np.exp(-LAM)], mode="markers", marker=dict(color=BLUE, size=11),
                             xaxis="x2", yaxis="y2"))
    fig.add_shape(type="rect", x0=ZOOM[0], x1=ZOOM[1], y0=0, y1=ZOOM[2], xref="x", yref="y", fillcolor="rgba(0,0,0,0)",
                  line=dict(color=GREY, dash="dot", width=2))
    fig.update_layout(xaxis=dict(domain=[0.0, 0.5], range=[-0.03, 3.05], dtick=0.5, title="distance along the beam z (m)"),
                      yaxis=dict(domain=[0.0, 0.84], range=[0, 2.15], title="chance ÷ cell length (per m)"),
                      xaxis2=dict(domain=[0.6, 1.0], anchor="y2", range=[ZOOM[0], ZOOM[1]], dtick=0.1, title="z (m), zoom: 0.8 to 1.3 m"),
                      yaxis2=dict(domain=[0.0, 0.84], anchor="x2", range=[0, ZOOM[2]], dtick=0.1))
    text(fig, 0.25, 0.93, "the whole beam; the wall is at 3 m", size=20, anchor="center")
    text(fig, 0.8, 0.93, "zoom on the dotted box", size=20, anchor="center")
    text(fig, 0.17, 0.74, "orange bar of cell j: (1 − b)<sup>j − 1</sup> b ÷ Δ", ORANGE, size=19)
    text(fig, 0.17, 0.66, "blue curve: λe<sup>−λz</sup> = 2e<sup>−2z</sup>", BLUE, size=19)
    text(fig, 0.17, 0.58, f"{round(WALL / d)} cells of {d:g} m", GREY, size=19)
    text(fig, 0.69, 0.78, f"red: cell from 1 m, {h[i1]:.3f} per m", RED, size=19)
    text(fig, 0.69, 0.70, f"blue: curve at 1 m, {LAM * np.exp(-LAM):.3f} per m", BLUE, size=19)
    title = f"cell length Δ = {d:g} m, so each cell is blocked with chance b = λΔ = 2 × {d:g} = {b:g}"
    sub = (f"cell from 1 m: {1 - b:g}<sup>{i1}</sup> × {b:g} ÷ {d:g} = {h[i1]:.3f} per m")
    fig.update_layout(template="simple_white", width=1150, height=620, font=FONT, showlegend=False, bargap=0, barmode="overlay",
                      margin=dict(l=90, r=30, t=105, b=75),
                      title=dict(text=f"{title}<br><span style='color:{RED}'>{sub}</span>", x=0.5, font_size=22))
    return fig


figs = [frame(d) for d in DELTAS]
make_gif(figs, here / "shrink_cells", fps=2, holds=[5, 3, 3, 5, 3, 12], keys=[0, 3, 5], cols=1, width=950)
assert [round(at1(d), 3) for d in (0.1, 0.01, 0.001)] == [0.215, 0.265, 0.270]
assert round(LAM * np.exp(-LAM), 3) == 0.271
assert round(0.8 ** 10 * 0.2 / 0.1, 3) == 0.215 and round(0.98 ** 100 * 0.02 / 0.01, 3) == 0.265
assert round(0.998 ** 1000 * 0.002 / 0.001, 3) == 0.270
