"""Why the step function cannot push (Plotly): the size of the update y - y_hat against the point's position z = w . x,
with y_hat from the step function. Every correctly placed point gives exactly 0 (no update); every misplaced point
gives +1 or -1, however near or far it is."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN

here = Path(__file__).parent
z = np.linspace(-5, 5, 1001)
step = (z > 0).astype(float)
assert np.all((1 - step)[z > 0] == 0) and np.all((0 - step)[z <= 0] == 0)
fig = go.Figure([go.Scatter(x=z, y=1 - step, mode="lines", line=dict(color=GREEN, width=5, shape="hv"), name="positive point (y = 1)"),
                 go.Scatter(x=z, y=0 - step, mode="lines", line=dict(color=BLUE, width=5, shape="hv"), name="negative point (y = 0)")])
fig.add_annotation(x=2.5, y=0.12, text="correct: update 0", showarrow=False, font=dict(size=19, color=GREEN))
fig.add_annotation(x=-2.5, y=1.12, text="wrong: update +1 at any distance", showarrow=False, font=dict(size=19, color=GREEN))
fig.add_annotation(x=-2.5, y=-0.12, text="correct: update 0", showarrow=False, font=dict(size=19, color=BLUE))
fig.add_annotation(x=2.5, y=-1.12, text="wrong: update −1 at any distance", showarrow=False, font=dict(size=19, color=BLUE))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT,
                  xaxis=dict(title="z = w · x   (negative side ← line → positive side)", zeroline=True),
                  yaxis=dict(title="y − ŷ with the step function", range=[-1.3, 1.3]),
                  legend=dict(x=0.6, y=0.75), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "step_update.png", scale=2)
