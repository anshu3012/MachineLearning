"""Regression (numerical output) vs classification (categorical output). Example data."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(3)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, subplot_titles=(
    "<b>Regression</b>: output is a number", "<b>Classification</b>: output is a category"))

# Regression: CGPA -> package (LPA)
cgpa = rng.uniform(5.5, 9.5, 40)
package = 1.4 * cgpa - 5 + rng.normal(0, 0.6, cgpa.size)
fig.add_trace(go.Scatter(x=cgpa, y=package, mode="markers", marker=dict(color=BLUE, size=11),
                         showlegend=False), 1, 1)
xs = np.array([5.5, 9.5]); m, b = np.polyfit(cgpa, package, 1)
fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=ORANGE, width=5),
                         showlegend=False), 1, 1)
fig.add_annotation(x=6.0, y=m * 6.0 + b + 1.6, text="predicted package<br>for any CGPA", showarrow=False,
                   font=dict(color=ORANGE, size=15), row=1, col=1)

# Classification: IQ, CGPA -> placed yes/no
iq = rng.uniform(70, 130, 60)
cg = rng.uniform(5.5, 9.5, 60)
score = 0.05 * iq + cg
THRESHOLD = np.median(score)
placed = (score + rng.normal(0, 0.1, 60)) > THRESHOLD
for flag, colour, name in [(True, GREEN, "Placed"), (False, RED, "Not placed")]:
    fig.add_trace(go.Scatter(x=iq[placed == flag], y=cg[placed == flag], mode="markers", name=name,
                             marker=dict(color=colour, size=11, symbol="circle" if flag else "x")), 1, 2)
xb = np.array([70, 130])
fig.add_trace(go.Scatter(x=xb, y=THRESHOLD - 0.05 * xb, mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                         name="boundary learned"), 1, 2)

fig.update_xaxes(title_text="CGPA", row=1, col=1)
fig.update_yaxes(title_text="Package (LPA)", row=1, col=1)
fig.update_xaxes(title_text="IQ", row=1, col=2)
fig.update_yaxes(title_text="CGPA", range=[5.3, 9.7], row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=560, font=dict(family="Roboto, Arial", size=17),
                  legend=dict(orientation="h", x=0.56, y=-0.2), margin=dict(l=70, r=20, t=80, b=110))
fig.update_annotations(font_size=19)
fig.add_annotation(x=1, y=-0.28, xref="paper", yref="paper", xanchor="right", showarrow=False,
                   text="example data", font=dict(size=13, color=GREY))
fig.write_image(here / "reg_vs_cls.png", scale=2)
fig.write_image(here / "reg_vs_cls.pdf")
