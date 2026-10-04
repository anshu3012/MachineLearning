"""Batch size trades memory against updates: observations held per update grow with batch_size,
updates per epoch on 320 observations shrink as ceil(320 / batch_size) (Plotly)."""
from math import ceil
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, ORANGE, RED, GREY, FONT

here = Path(__file__).parent
N = 320
bs = list(range(1, N + 1))
upd = [ceil(N / b) for b in bs]
assert upd[0] == 320 and upd[31] == 10 and upd[-1] == 1          # the Note's table in section 6
fig = go.Figure()
fig.add_trace(go.Scatter(x=bs, y=bs, name="observations in memory per update", line=dict(color=GREY, width=3)))
fig.add_trace(go.Scatter(x=bs, y=upd, name="updates per epoch", line=dict(color=BLUE, width=3, shape="hv")))
for b, name, c in ((1, "stochastic", RED), (32, "mini-batch", ORANGE), (320, "batch", BLUE)):
    fig.add_trace(go.Scatter(x=[b, b], y=[b, ceil(N / b)], mode="markers+text", showlegend=False,
                             marker=dict(size=14, color=c), text=[f"{name}: {b} in memory", f"{ceil(N / b)} update" + ("s" if b < 320 else "")],
                             textposition={1: ["middle right", "bottom right"], 32: ["middle right", "middle right"],
                                           320: ["middle left", "middle left"]}[b],
                             textfont=dict(size=17, color=c)))
fig.update_layout(template="simple_white", width=860, height=520, font=dict(FONT, size=18),
                  xaxis=dict(type="log", title="batch_size (log scale)", tickvals=[1, 10, 32, 100, 320]),
                  yaxis=dict(type="log", title="count (log scale)", tickvals=[1, 10, 32, 100, 320]),
                  legend=dict(x=0.25, y=1.12, orientation="h"), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "memory_tradeoff.png", scale=2)
fig.write_image(here / "memory_tradeoff.pdf")
