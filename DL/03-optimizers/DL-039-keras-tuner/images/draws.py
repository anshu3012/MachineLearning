"""Sections 6 and 7: the values hp.Int can draw (grey ticks) and the 5 values the random search drew, with their
validation accuracy. Horizontal lines in the layers plot are steps of one patient, 1/154 (Plotly)."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, GREEN, GREY, FONT

here = Path(__file__).parent
units = {56: 0.773, 104: 0.766, 64: 0.753, 32: 0.734, 8: 0.636}             # section 6 table
layers = {3: 0.766, 5: 0.766, 10: 0.753, 1: 0.740, 8: 0.734}                 # section 7 table
grid_u, grid_l = list(range(8, 129, 8)), list(range(1, 11))
assert len(grid_u) == 16 and set(units) <= set(grid_u) and set(layers) <= set(grid_l)
for a in layers.values():                                                     # every score is k / 154
    assert abs(round(a * 154) / 154 - a) < 6e-4


def plot(vals, grid, xtitle, name, ylo, step_lines=False):
    best = max(vals, key=vals.get)
    fig = go.Figure()
    if step_lines:
        for k in range(int(ylo * 154), 120):
            fig.add_hline(y=k / 154, line=dict(color="#BBBBBB", width=1, dash="dot"))
    fig.add_trace(go.Scatter(x=grid, y=[ylo + 0.004] * len(grid), mode="markers",
                             marker=dict(symbol="line-ns-open", size=16, color=GREY, line=dict(width=2)),
                             name=f"possible values ({len(grid)})"))
    fig.add_trace(go.Scatter(x=list(vals), y=list(vals.values()), mode="markers+text", name="drawn by the search (5)",
                             marker=dict(size=18, color=[GREEN if (v == vals[best]) else BLUE for v in vals.values()]),
                             text=[f"{a:.3f}" for a in vals.values()], textposition="top center",
                             textfont=dict(size=18)))
    if step_lines:
        fig.add_annotation(x=6.5, y=0.776, showarrow=False, font=dict(size=17, color=GREY),
                           text="dotted lines: one patient apart (1/154 = 0.0065)")
    fig.update_layout(template="simple_white", width=900, height=470, font=dict(FONT, size=18),
                      xaxis=dict(title=xtitle, tickvals=grid if len(grid) <= 10 else grid[::2]),
                      yaxis=dict(title="validation accuracy", range=[ylo, max(vals.values()) + 0.02]),
                      legend=dict(orientation="h", x=0, y=1.12), margin=dict(l=80, r=20, t=50, b=60))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


plot(units, grid_u, "nodes in the hidden layer (hp.Int, 8 to 128, step 8)", "units_draws", 0.62)
plot(layers, grid_l, "hidden layers (hp.Int, 1 to 10)", "layers_draws", 0.725, step_lines=True)
