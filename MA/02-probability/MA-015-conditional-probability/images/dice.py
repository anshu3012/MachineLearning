"""Two dice: the 36 outcomes, the event B = (sum <= 10), and A = (die 1 = 5) inside B (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
d = np.arange(1, 7)
S = d[:, None] + d[None, :]           # rows: die 1, columns: die 2
A = np.zeros((6, 6), bool); A[4, :] = True        # die 1 = 5
B = S <= 10
panels = [("All 36 outcomes (numbers = sum)", np.ones((6, 6))),
          ("B: sum ≤ 10 (33 outcomes)", np.where(B, 1, 0.15)),
          ("A ∩ B: die 1 = 5 within B (5 outcomes)", np.where(A & B, 2, np.where(B, 1, 0.15)))]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06, subplot_titles=[p[0] for p in panels])
scale = [[0, "#F4F4F4"], [0.07, "#F4F4F4"], [0.5, "#DCE6F2"], [1, "#E45756"]]
for k, (_, z) in enumerate(panels):
    fig.add_trace(go.Heatmap(z=z, x=d, y=d, colorscale=scale, zmin=0, zmax=2, showscale=False, xgap=3, ygap=3,
                             text=S, texttemplate="%{text}", textfont=dict(size=15), hoverinfo="skip"), 1, k + 1)
fig.update_xaxes(title="die 2", dtick=1)
fig.update_yaxes(dtick=1, autorange="reversed")
fig.update_yaxes(title="die 1", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=440, font=dict(family="Latin Modern Roman", size=15),
                  margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "dice.png", scale=2); fig.write_image(here / "dice.pdf")
print("P(A)", A.mean(), "P(B)", B.sum(), "/36", "P(A and B)", (A & B).sum(), "/36", "P(A|B)", (A & B).sum(), "/", B.sum())
