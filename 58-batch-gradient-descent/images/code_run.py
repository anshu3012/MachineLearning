"""What the Section 4 code produces (Plotly): test R2 after each epoch of the GDRegressor run (learning rate 0.5),
against the exact OLS value 0.440, and the intercept heading for 152."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE
from run58 import HIST, ols

here = Path(__file__).parent
e = np.arange(len(HIST))
r2 = [h[2] for h in HIST]
b0 = [h[0] for h in HIST]
fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=["test R² after each epoch", "intercept β₀"])
fig.update_annotations(font_size=22)
fig.add_trace(go.Scatter(x=e[1:], y=r2[1:], mode="lines", line=dict(color=BLUE, width=4), name="gradient descent"), 1, 1)
fig.add_trace(go.Scatter(x=[1, 1000], y=[0.440] * 2, mode="lines",
                         line=dict(color=ORANGE, dash="dash", width=3), name="OLS"), 1, 1)
fig.add_trace(go.Scatter(x=e[1:], y=b0[1:], mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[1, 1000], y=[ols.intercept_] * 2, mode="lines", line=dict(color=ORANGE, dash="dash", width=3),
                         showlegend=False), 1, 2)
fig.update_xaxes(type="log", title="epoch (log scale)")
fig.update_yaxes(title="test R²", range=[-0.05, 0.55], row=1, col=1)
fig.update_yaxes(title="β₀", row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=30, t=60, b=120))
fig.write_image(here / "code_run.png", scale=2)
assert next(i for i, v in enumerate(r2) if v >= 0.44) == 407 and round(b0[1], 1) == 150.5
