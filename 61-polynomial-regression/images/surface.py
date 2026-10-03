"""Two inputs: z = x^2 + y^2 + 0.2x + 0.2y + 0.1xy + 2 + noise. A plane (linear regression) vs a degree-2 surface (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

here = Path(__file__).parent
rng = np.random.default_rng(1)
x = 7 * rng.random(100) - 2.8; y = 7 * rng.random(100) - 2.8
z = x ** 2 + y ** 2 + 0.2 * x + 0.2 * y + 0.1 * x * y + 2 + rng.standard_normal(100)
XY = np.c_[x, y]                                 # the two inputs side by side
g = np.linspace(-2.8, 4.2, 25); G1, G2 = np.meshgrid(g, g); grid = np.c_[G1.ravel(), G2.ravel()]
models = [("Linear regression: a plane", LinearRegression()),
          ("Degree 2: a curved surface", make_pipeline(PolynomialFeatures(2), LinearRegression()))]
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "scene"}]], horizontal_spacing=0.02,
                    subplot_titles=[f"{t}, R² {m.fit(XY, z).score(XY, z):.2f}" for t, m in models])
for col, (_, m) in enumerate(models, start=1):
    fig.add_trace(go.Surface(x=G1, y=G2, z=m.predict(grid).reshape(G1.shape), opacity=0.55, showscale=False,
                             colorscale=[[0, "#F58518"], [1, "#F58518"]]), 1, col)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=dict(size=3, color="#4C78A8")), 1, col)
cam = dict(eye=dict(x=1.7, y=-1.6, z=0.8))
fig.update_scenes(xaxis_title="x", yaxis_title="y", zaxis_title="z", camera=cam, aspectmode="cube")
fig.update_layout(template="simple_white", width=1150, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=14), margin=dict(l=0, r=0, t=50, b=0))
fig.update_annotations(font_size=17)
print([round(m.score(XY, z), 3) for _, m in models])
fig.write_image(here / "surface.png", scale=2)
fig.write_image(here / "surface.pdf")
