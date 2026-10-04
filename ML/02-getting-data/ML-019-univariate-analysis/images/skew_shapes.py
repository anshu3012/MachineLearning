"""Three shapes of data: right-skewed (salaries), symmetric (normal), left-skewed (easy-test marks).
Made-up curves, drawn to show where the mean sits compared with the median."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
x = np.linspace(0, 1, 400)
shapes = [("Right (positive) skew<br>e.g. salaries", stats.beta(1.6, 6)),
          ("Symmetric (skew = 0)<br>e.g. a normal distribution", stats.beta(5, 5)),
          ("Left (negative) skew<br>e.g. marks in an easy test", stats.beta(6, 1.6))]
fig = make_subplots(1, 3, subplot_titles=[s[0] for s in shapes], horizontal_spacing=0.06)
for i, (_, d) in enumerate(shapes, start=1):
    fig.add_trace(go.Scatter(x=x, y=d.pdf(x), fill="tozeroy", line=dict(color="#4C78A8", width=3),
                             fillcolor="rgba(76,120,168,0.18)"), 1, i)
    for val, colour, name, shift in [(d.mean(), "#F58518", "mean", 12), (d.median(), "#54A24B", "median", -12)]:
        fig.add_vline(x=val, line=dict(color=colour, width=2.5, dash="dash"), opacity=1, row=1, col=i)
        if i != 2 or name == "mean":
            fig.add_annotation(x=val, y=3.95, text=name if i != 2 else "mean = median", showarrow=False,
                               xshift=shift * (1 if i != 3 else -1) * (2.6 if i != 2 else 0),
                               font=dict(color=colour if i != 2 else "#6B6B6B", size=20), row=1, col=i)
    fig.update_xaxes(showticklabels=False, title="value", row=1, col=i)
    fig.update_yaxes(showticklabels=False, range=[0, 4.2], row=1, col=i)
fig.update_yaxes(title="how common", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=400, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=22), margin=dict(l=50, r=20, t=80, b=50))
fig.update_annotations(font_size=21)
fig.write_image(here / "skew_shapes.png", scale=2)
fig.write_image(here / "skew_shapes.pdf")
