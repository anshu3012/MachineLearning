"""Two conditional probabilities on the 36 outcomes of two dice: reduce to B, count A inside it (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
d = np.arange(1, 7)
S = d[:, None] + d[None, :]                     # rows: die 1, columns: die 2
D1 = np.repeat(d[:, None], 6, axis=1)
cases = [("B: die 1 odd (18); A: sum = 7 (3)", D1 % 2 == 1, S == 7),
         ("B: sum ≤ 5 (10); A: die 1 = 2 (3)", S <= 5, D1 == 2)]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=[c[0] for c in cases])
scale = [[0, "#F4F4F4"], [0.07, "#F4F4F4"], [0.5, "#DCE6F2"], [1, "#E45756"]]
for k, (_, B, A) in enumerate(cases):
    z = np.where(A & B, 2, np.where(B, 1, 0.15))
    print(k, (A & B).sum(), B.sum())
    fig.add_trace(go.Heatmap(z=z, x=d, y=d, colorscale=scale, zmin=0, zmax=2, showscale=False, xgap=3, ygap=3,
                             text=S, texttemplate="%{text}", textfont=dict(size=18), hoverinfo="skip"), 1, k + 1)
fig.update_xaxes(title="die 2", dtick=1)
fig.update_yaxes(dtick=1, autorange="reversed")
fig.update_yaxes(title="die 1", row=1, col=1)
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=60, r=20, t=50, b=60))
for a in fig.layout.annotations:
    a.font.size = 21
fig.write_image(here / "dice_conditional.png", scale=2)
fig.write_image(here / "dice_conditional.pdf")
