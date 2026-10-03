"""Note 96 figures (Plotly): kernels.png - decision regions of four SVMs on the circles data;
app_preview.png - the Dash app."""
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

# 2. a preview of the Dash app with its default settings
fig = figure_for("circles", "rbf", 0, 0, 3)
fig.update_layout(width=640, height=560, font=dict(family="Latin Modern Roman", size=16))
fig.write_image(here / "app_preview.png", scale=2)
