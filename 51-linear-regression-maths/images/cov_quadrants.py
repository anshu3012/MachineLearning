"""What the slope formula adds up, on the 160 training students (Plotly). Axes are moved to the point of means.
Each student contributes (x - x-bar)(y - y-bar): positive (blue) in the top-right and bottom-left quarters, negative
(red) in the other two. Their sum, 101.204, over the sum of (x - x-bar)^2, 181.384, is the slope 0.558."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import M, X_train, y_train
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
dx, dy = x - x.mean(), y - y.mean()
top, bottom = (dx * dy).sum(), (dx ** 2).sum()
assert round(top, 3) == 101.204 and round((dx * dy)[dx * dy > 0].sum(), 2) == 103.06 and round(bottom, 3) == 181.384 and abs(top / bottom - M) < 1e-12
p = dx * dy > 0
fig = go.Figure()
fig.add_shape(type="rect", x0=0, y0=0, x1=3, y1=2, fillcolor=BLUE, opacity=0.07, line_width=0)
fig.add_shape(type="rect", x0=-3, y0=-2, x1=0, y1=0, fillcolor=BLUE, opacity=0.07, line_width=0)
fig.add_shape(type="rect", x0=-3, y0=0, x1=0, y1=2, fillcolor=RED, opacity=0.07, line_width=0)
fig.add_shape(type="rect", x0=0, y0=-2, x1=3, y1=0, fillcolor=RED, opacity=0.07, line_width=0)
for mask, c, name in ((p, BLUE, f"product > 0: {p.sum()} students"), (~p, RED, f"product < 0: {(~p).sum()} students")):
    fig.add_scatter(x=dx[mask], y=dy[mask], mode="markers", name=name,
                    marker=dict(size=4 + 14 * np.sqrt(np.abs(dx * dy)[mask]), color=c, opacity=0.75,
                                line=dict(color="white", width=1)))
for (tx, ty, t, c) in ((0.9, 1.8, "+ × + = +", BLUE), (-0.8, -1.8, "− × − = +", BLUE),
                       (-2.2, 1.7, "− × + = −", RED), (2.2, -1.7, "+ × − = −", RED)):
    fig.add_annotation(x=tx, y=ty, text=t, showarrow=False, font=dict(size=24, color=c))
fig.add_annotation(x=0.5, y=1.12, xref="paper", yref="paper", showarrow=False, font=dict(size=24),
                   text=f"sum of products = {top:.3f}   ÷   sum of (x − x̄)² = {bottom:.3f}   =   slope m = {M:.3f}")
fig.update_layout(template="simple_white", width=1000, height=680, font=FONT,
                  xaxis=dict(title="x − x̄  (CGPA above or below its mean)", range=[-3, 3], zeroline=True, zerolinewidth=2),
                  yaxis=dict(title="y − ȳ  (package above or below its mean)", range=[-2, 2], zeroline=True, zerolinewidth=2),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=90, r=30, t=90, b=130))
fig.write_image(here / "cov_quadrants.png", scale=2)
