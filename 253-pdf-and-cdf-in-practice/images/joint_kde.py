"""2D density plot of petal length and sepal length (all 150 iris flowers): filled contours of a 2D KDE, with the
1D KDE of each column on its edge. Darker = higher density, like the peaks of a mountain seen from above."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.datasets import load_iris

here = Path(__file__).parent
d = load_iris().data
x, y = d[:, 2], d[:, 0]                       # petal length, sepal length
gx, gy = np.linspace(0, 8, 160), np.linspace(3.5, 8.5, 160)
X, Y = np.meshgrid(gx, gy)
Z = stats.gaussian_kde(np.vstack([x, y]))(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
fig = make_subplots(rows=2, cols=2, column_widths=[0.82, 0.18], row_heights=[0.2, 0.8], shared_xaxes=True,
                    shared_yaxes=True, horizontal_spacing=0.02, vertical_spacing=0.02)
fig.add_contour(x=gx, y=gy, z=Z, colorscale=[[0, "white"], [0.1, "#DEEBF7"], [0.5, "#6BAED6"], [1, "#08306B"]], contours=dict(start=0.02, end=0.22, size=0.02), zmin=0, zmax=0.22, line=dict(width=0.5),
                colorbar=dict(title=dict(text="density", side="right"), x=1.02, len=0.75, y=0.4), row=2, col=1)
fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color="#F58518", size=4, opacity=0.6), row=2, col=1)
fig.add_scatter(x=gx, y=stats.gaussian_kde(x)(gx), mode="lines", line=dict(color="#4C78A8", width=3), row=1, col=1)
fig.add_scatter(x=stats.gaussian_kde(y)(gy), y=gy, mode="lines", line=dict(color="#4C78A8", width=3), row=2, col=2)
fig.update_xaxes(title_text="petal length (cm)", row=2, col=1)
fig.update_yaxes(title_text="sepal length (cm)", row=2, col=1)
fig.update_xaxes(showticklabels=False, row=2, col=2)
fig.update_yaxes(showticklabels=False, row=1, col=1)
fig.update_layout(template="simple_white", width=900, height=650, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=20, b=50))
fig.write_image(here / "joint_kde.png", scale=2)
fig.write_image(here / "joint_kde.pdf")
