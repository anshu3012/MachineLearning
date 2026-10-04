"""Loss of y = m x + b over (m, b) for a dense feature (left) and for the sparse IIT feature (right) (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, FONT
from shared import DATA, X as Xs, y as ys, BEST

here = Path(__file__).parent
dn = pd.read_csv(DATA / "dense.csv")
Xd, yd = np.c_[dn.x, np.ones(len(dn))], dn.y.to_numpy()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("dense feature: round bowl", "sparse feature (90% zeros): elongated bowl"))
for col, (X, y) in enumerate(((Xd, yd), (Xs, ys)), start=1):
    best = np.linalg.lstsq(X, y, rcond=None)[0]
    m = np.linspace(best[0] - 10, best[0] + 10, 160)
    b = np.linspace(best[1] - 10, best[1] + 10, 160)
    M, B = np.meshgrid(m, b)
    Z = ((y[None, None, :] - M[..., None] * X[:, 0] - B[..., None]) ** 2).mean(-1)
    fig.add_trace(go.Contour(x=m, y=b, z=np.log10(Z), colorscale="Greys", reversescale=True, showscale=False,
                             contours=dict(start=-0.6, end=2.4, size=0.2), line=dict(width=0.6), opacity=0.6),
                  row=1, col=col)
    fig.add_trace(go.Scatter(x=[best[0]], y=[best[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=16, color=RED)), row=1, col=col)
fig.update_xaxes(title_text="m (weight of the feature)")
fig.update_yaxes(title_text="b (bias)", col=1)
fig.update_layout(template="simple_white", width=1000, height=480, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "sparse_bowl.png", scale=2)
fig.write_image(here / "sparse_bowl.pdf")
