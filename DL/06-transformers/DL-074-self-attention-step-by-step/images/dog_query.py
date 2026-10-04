"""Section 7's invented example: the query of "dog" points along the first axis; the keys of "old" and "brown" point
mostly the same way, the keys of "the" and "dog" along the second axis. Left: the vectors. Right: scores q.k and the
softmax weights. Numbers from the text (asserted). Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
q = np.array([3, 0])
K = {"the": (0, 2), "old": (3, 0.5), "brown": (2.8, 1), "dog": (0.2, 2)}
s = np.array([q @ np.array(k) for k in K.values()])
w = np.exp(s) / np.exp(s).sum()
assert np.allclose(s, [0, 9, 8.4, 0.6]) and np.allclose(w.round(3), [0.000, 0.646, 0.354, 0.000])
fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.12,
                    subplot_titles=("query of \"dog\" and the four keys", "scores q · k and weights after softmax"))
cols = {"the": GREY, "old": GREEN, "brown": ORANGE, "dog": BLUE}
for name, k in K.items():
    fig.add_annotation(x=k[0], y=k[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowwidth=3, arrowcolor=cols[name], text="")
    fig.add_annotation(x=k[0], y=k[1], text=f"key {name}", showarrow=False, xshift={"the": -42, "dog": 46}.get(name, 40),
                       yshift=8, font=dict(size=18, color=cols[name]), xref="x", yref="y")
fig.add_annotation(x=3, y=0, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2,
                   arrowwidth=5, arrowcolor=RED, text="")
fig.add_annotation(x=3, y=0, text="query dog", showarrow=False, yshift=-18, font=dict(size=18, color=RED), xref="x", yref="y")
fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(size=1), showlegend=False, row=1, col=1)
fig.update_xaxes(range=[-0.3, 4.4], row=1, col=1)
fig.update_yaxes(range=[-0.6, 2.6], scaleanchor="x", row=1, col=1)
names = list(K)
fig.add_bar(x=names, y=s, name="score q · k", marker_color="#C9C9C9", text=[f"{v:g}" for v in s],
            textposition="outside", row=1, col=2)
fig.add_bar(x=names, y=w * 10, name="weight (x 10)", marker_color=[cols[n] for n in names],
            text=[f"{v:.3f}" for v in w], textposition="outside", row=1, col=2)
fig.update_yaxes(range=[0, 11], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=dict(FONT, size=18), barmode="group",
                  legend=dict(x=0.6, y=1.0), margin=dict(l=40, r=20, t=50, b=40))
fig.write_image(here / "dog_query.png", scale=2)
fig.write_image(here / "dog_query.pdf")
