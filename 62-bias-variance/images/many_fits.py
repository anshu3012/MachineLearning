"""Each model trained on 20 different random training sets of 40 points (Plotly): the spread of the curves is the
variance; how far their average is from the truth is the bias."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import fits, decompose, f, xs

here = Path(__file__).parent
cases = [(1, "Degree 1: high bias, low variance"), (5, "Degree 5: low bias, low variance"),
         (11, "Degree 11: low bias, high variance")]
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.03, subplot_titles=[c[1] for c in cases])
for col, (d, _) in enumerate(cases, start=1):
    P = fits(d)
    for p in P[:20]:
        fig.add_trace(go.Scatter(x=xs, y=np.clip(p, -4, 4), mode="lines", line=dict(color="#F58518", width=1), opacity=0.45), 1, col)
    fig.add_trace(go.Scatter(x=xs, y=f(xs), mode="lines", line=dict(color="black", width=3, dash="dash")), 1, col)
    fig.add_trace(go.Scatter(x=xs, y=np.clip(P.mean(axis=0), -4, 4), mode="lines", line=dict(color="#4C78A8", width=3)), 1, col)
    b2, v = decompose(P)
    fig.add_annotation(x=0, y=-3.5, xref=f"x{'' if col == 1 else col}", yref="y", showarrow=False,
                       text=f"bias² {b2:.3f}, variance {v:.3f}", font=dict(size=15))
    fig.update_xaxes(title="x", row=1, col=col)
    print(d, round(b2, 3), round(v, 3))
fig.update_yaxes(title="y", range=[-4, 4], row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=14), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=15, selector=dict(xref="paper"))
fig.write_image(here / "many_fits.png", scale=2)
fig.write_image(here / "many_fits.pdf")
