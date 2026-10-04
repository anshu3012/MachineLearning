"""What a residual is, on the Note's 60 test observations (Plotly): actual target against predicted target. Each
stick is one residual y - y-hat, the vertical gap to the diagonal of perfect predictions; blue above, red below.
Assumptions 3 to 5 are about these 60 sticks."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import residual, y_pred, y_test
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
assert len(residual) == 60 and round(1 - (residual ** 2).sum() / ((y_test - y_test.mean()) ** 2).sum(), 2) == 0.96
fig = go.Figure()
lo, hi = min(y_pred.min(), y_test.min()), max(y_pred.max(), y_test.max())
pad = 0.05 * (hi - lo)
fig.add_scatter(x=[lo - pad, hi + pad], y=[lo - pad, hi + pad], mode="lines", line=dict(color=GREY, dash="dash", width=2),
                name="perfect prediction (actual = predicted)")
for m, c, name in ((residual > 0, BLUE, "residual > 0 (actual above)"), (residual <= 0, RED, "residual < 0 (actual below)")):
    sx, sy = [], []
    for p, a in zip(y_pred[m], y_test[m]):
        sx += [p, p, None]; sy += [p, a, None]
    fig.add_scatter(x=sx, y=sy, mode="lines", line=dict(color=c, width=3), name=name)
fig.add_scatter(x=y_pred, y=y_test, mode="markers", marker=dict(size=9, color="black"), name="test observation")
fig.update_layout(template="simple_white", width=900, height=650, font=dict(FONT, size=20),
                  xaxis=dict(title="predicted target ŷ", range=[lo - pad, hi + pad]),
                  yaxis=dict(title="actual target y", range=[lo - pad, hi + pad], scaleanchor="x"),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "residuals_def.png", scale=2)
