"""Test accuracy on the heart data: three base models alone, soft voting, and four ways of stacking (Plotly).
Numbers come from notebook.ipynb (KNN scaled; 61 test patients, so one patient = 1.6 points)."""
from pathlib import Path

import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
rows = [("random forest", 0.787, "#4C78A8"), ("KNN (scaled)", 0.836, "#4C78A8"), ("gradient boosting", 0.852, "#4C78A8"),
        ("soft voting", 0.885, "#6B6B6B"), ("blending (hold-out)", 0.820, "#E45756"),
        ("K-fold stacking by hand", 0.869, "#E45756"), ("StackingClassifier", 0.869, "#E45756"),
        ("StackingClassifier, passthrough", 0.852, "#E45756")]
fig = go.Figure(go.Bar(y=[r[0] for r in rows][::-1], x=[r[1] for r in rows][::-1], orientation="h",
                       marker_color=[r[2] for r in rows][::-1], text=[f"{r[1]:.3f}" for r in rows][::-1],
                       textposition="outside"))
fig.update_xaxes(title="test accuracy (61 patients)", range=[0.7, 0.93])
fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, margin=dict(l=20, r=30, t=20, b=70))
fig.write_image(HERE / "accuracies.png", scale=2)
fig.write_image(HERE / "accuracies.pdf")
