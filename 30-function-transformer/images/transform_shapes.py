"""What each transform does to a number line: the curves of log(1 + x), sqrt(x), x^2 and 1/x, and where the Note's
example values land. The log and square root squash big values; the square stretches them; the reciprocal flips."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
fares = np.array([7.25, 71.28, 512.33])
assert list(np.log1p(fares).round(2)) == [2.11, 4.28, 6.24] and list(np.sqrt(fares).round(2)) == [2.69, 8.44, 22.63]
assert list((1 / np.array([2, 4, 10, 100])).round(2)) == [0.5, 0.25, 0.1, 0.01]
P = [("log(1 + x): big values shrink a lot", np.log1p, fares, "#54A24B"),
     ("√x: big values shrink, more gently", np.sqrt, fares, "#4C78A8"),
     ("x²: big values stretch apart (marks)", np.square, np.array([30, 80, 90.0]), "#F58518"),
     ("1/x: the order flips", lambda v: 1 / v, np.array([2, 4, 10, 100.0]), "#B279A2")]
fmt = lambda y: f"{y:,.0f}" if y >= 1000 else f"{y:.3g}"
fig = make_subplots(rows=1, cols=4, horizontal_spacing=0.07, subplot_titles=[p[0] for p in P])
for j, (_, f, v, c) in enumerate(P, start=1):
    lo, hi = (0.8, 110) if j == 4 else (0, v.max() * 1.05)
    if j == 3:
        fig.update_xaxes(range=[0, 112], row=1, col=3)
    g = np.linspace(lo, hi, 400)
    fig.add_scatter(x=g, y=f(g), mode="lines", line=dict(color=c, width=4), row=1, col=j)
    fig.add_scatter(x=v, y=f(v), mode="markers+text", marker=dict(size=12, color="black"),
                    text=[f"{a:g} → {fmt(f(a))}" for a in v],
                    textposition=["bottom right"] * (len(v) - 1) + ["top left"] if j < 4 else ["top right"] * 3 + ["top left"],
                    textfont=dict(size=14), cliponaxis=False, row=1, col=j)
    fig.update_xaxes(title_text="x", row=1, col=j)
fig.update_yaxes(title_text="transformed x′", row=1, col=1)
fig.update_xaxes(type="log", tickvals=[1, 2, 4, 10, 100], row=1, col=4)
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1600, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "transform_shapes.png", scale=2)
fig.write_image(here / "transform_shapes.pdf")
