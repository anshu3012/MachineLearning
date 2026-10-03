"""Note 96 figures (Plotly): kernels.png - decision regions of four SVMs on the circles data;
lift.png - the transformation exp(-x^2) per coordinate, in 2D and summed into a 3D height; app_preview.png - the Dash app."""
import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

here = Path(__file__).parent
sys.path.insert(0, str(here.parent))
from app import COLOURS, figure_for, make_data, traces  # noqa: E402

font = dict(family="Latin Modern Roman", size=18)
X, y = make_data("circles")
a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=0)

# 1. four kernels
models = [("linear kernel", dict(kernel="linear")), ("RBF kernel", dict(kernel="rbf")),
          ("polynomial kernel, degree 3", dict(kernel="poly", degree=3)),
          ("polynomial kernel, degree 2", dict(kernel="poly", degree=2))]
fitted = [(name, SVC(**kw).fit(a, c)) for name, kw in models]
fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.08, vertical_spacing=0.15,
                    subplot_titles=[f"{n}: test accuracy {m.score(b, d):.2f}" for n, m in fitted])
for k, (name, m) in enumerate(fitted):
    for t in traces(m, X, y, showlegend=k == 0):
        fig.add_trace(t, k // 2 + 1, k % 2 + 1)
    print(name, "test accuracy", m.score(b, d), "support vectors", len(m.support_vectors_))
fig.update_xaxes(title="x₁", range=[-1.4, 1.4])
fig.update_yaxes(range=[-1.4, 1.4])
fig.update_yaxes(title="x₂", col=1)
fig.update_layout(template="simple_white", width=900, height=900, font=font, margin=dict(l=60, r=20, t=50, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08))
fig.update_annotations(font_size=18)
fig.write_image(here / "kernels.png", scale=2); fig.write_image(here / "kernels.pdf")

# 2. the lift used in the code: X_new = exp(-X**2) per coordinate, z = their sum
X_new = np.exp(-(X ** 2))
z = X_new.sum(axis=1)
fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.06,
                    specs=[[{"type": "xy"}, {"type": "scene"}]],
                    subplot_titles=("each coordinate through exp(−x²)", "z = exp(−x₁²) + exp(−x₂²) as a height"))
for cls, name in ((0, "outer ring (class 0)"), (1, "centre (class 1)")):
    m = y == cls
    fig.add_trace(go.Scatter(x=X_new[m, 0], y=X_new[m, 1], mode="markers", name=name,
                             marker=dict(color=COLOURS[cls], size=8, line=dict(color="white", width=0.5))), 1, 1)
    fig.add_trace(go.Scatter3d(x=X[m, 0], y=X[m, 1], z=z[m], mode="markers", showlegend=False,
                               marker=dict(color=COLOURS[cls], size=4)), 1, 2)
g = np.linspace(-1.3, 1.3, 2)
fig.add_trace(go.Surface(x=g, y=g, z=np.full((2, 2), 1.75), showscale=False, opacity=0.35,
                         colorscale=[[0, "#B279A2"], [1, "#B279A2"]], hoverinfo="skip"), 1, 2)
fig.update_xaxes(title="exp(−x₁²)", range=[0.15, 1.05], row=1, col=1)
fig.update_yaxes(title="exp(−x₂²)", range=[0.15, 1.05], scaleanchor="x", row=1, col=1)
fig.update_scenes(xaxis_title="x₁", yaxis_title="x₂", zaxis_title="z", camera=dict(eye=dict(x=1.5, y=-1.5, z=0.7)),
                  aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.8),
                  xaxis_tickfont_size=12, yaxis_tickfont_size=12, zaxis_tickfont_size=12)
fig.update_layout(template="simple_white", width=1100, height=520, font=font, margin=dict(l=60, r=20, t=50, b=60),
                  legend=dict(orientation="h", x=0.2, xanchor="center", y=-0.18))
fig.update_annotations(font_size=18)
fig.write_image(here / "lift.png", scale=2); fig.write_image(here / "lift.pdf")
print("z outer", z[y == 0].min().round(2), z[y == 0].max().round(2), "z centre", z[y == 1].min().round(2))

# 3. a preview of the Dash app with its default settings
fig = figure_for("circles", "rbf", 0, 0, 3)
fig.update_layout(width=640, height=560, font=dict(family="Latin Modern Roman", size=16))
fig.write_image(here / "app_preview.png", scale=2)
