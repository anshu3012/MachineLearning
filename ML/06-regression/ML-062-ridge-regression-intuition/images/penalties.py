"""The three penalties of regularised linear regression for one coefficient beta (Plotly): Ridge (L2) beta^2,
Lasso (L1) |beta|, and Elastic Net, here half of each. All are 0 at beta = 0 and grow with the size of beta; the
square grows slowly near 0 and fast far out, the absolute value at a constant rate with a corner at 0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE

here = Path(__file__).parent
b = np.linspace(-3, 3, 601)
curves = [(b ** 2, BLUE, "Ridge (L2): β²"), (np.abs(b), ORANGE, "Lasso (L1): |β|"),
          (0.5 * b ** 2 + 0.5 * np.abs(b), GREEN, "Elastic Net: ½β² + ½|β|")]
assert curves[0][0][300] == curves[1][0][300] == curves[2][0][300] == 0
fig = go.Figure([go.Scatter(x=b, y=y, mode="lines", line=dict(color=c, width=5), name=n) for y, c, n in curves])
fig.update_layout(template="simple_white", width=950, height=560, font=FONT,
                  xaxis=dict(title="coefficient β", zeroline=True), yaxis=dict(title="penalty added to the loss", range=[-0.2, 6]),
                  legend=dict(x=0.35, y=0.99), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "penalties.png", scale=2)
