"""Which numbers of the band's least-squares problem can be non-zero. Left: the band of 10 poses in the cycle the
person is first seen; its 33 unknowns in TEB's order (dT1, then x, y, theta of pose 2, dT2, ...; poses 1 and 10 are
fixed) label the rows and columns of the matrix J^T J that every Levenberg-Marquardt step solves. A dark cell is an
entry that can be non-zero, because some cost term uses both unknowns: 47 percent of the cells. Right: the same
pattern for a band of 47 poses (181 unknowns), the size of the example in Roesmann et al. 2013: 9.7 percent. Each
term uses only neighbouring poses and time steps, so the dark cells hug the diagonal, and the longer the band, the
emptier the matrix. Run -> sparsity.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT
from plotly.subplots import make_subplots

here = Path(__file__).parent
n = len(bk.results()["loop"][24]["P"])
M10, names = bk.sparsity(n)
M47, names47 = bk.sparsity(47)
assert n == 10 and len(names) == 33 and round(100 * M10.mean()) == 47
assert len(names47) == 181 and round(100 * M47.mean(), 1) == 9.7
lab = [("ΔT" + s[1:]) if s[0] == "T" else (s.replace("t", "θ", 1) if s[0] == "t" else s) for s in names]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=[f"10 poses, 33 unknowns: {100 * M10.mean():.0f} percent",
                                    f"47 poses, 181 unknowns: {100 * M47.mean():.1f} percent"])
cs = [[0, "white"], [1, "#4C78A8"]]
fig.add_trace(go.Heatmap(z=M10[::-1].astype(int), x=lab, y=lab[::-1], colorscale=cs, showscale=False, xgap=1, ygap=1),
              row=1, col=1)
fig.add_trace(go.Heatmap(z=M47[::-1].astype(int), colorscale=cs, showscale=False), row=1, col=2)
fig.update_xaxes(tickangle=-90, tickfont=dict(size=11), row=1, col=1)
fig.update_yaxes(tickfont=dict(size=11), row=1, col=1)
fig.update_xaxes(visible=False, row=1, col=2)
fig.update_yaxes(visible=False, scaleanchor="x2", row=1, col=2)
fig.update_yaxes(scaleanchor="x", row=1, col=1)
fig.add_shape(type="rect", x0=-0.5, x1=180.5, y0=-0.5, y1=180.5, xref="x2", yref="y2", line=dict(color="#555555", width=1.5))
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", font=FONT, width=1400, height=760, margin=dict(l=60, r=20, t=60, b=70))
fig.write_image(here / "sparsity.png", scale=2)
