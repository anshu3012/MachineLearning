"""Why two-point fits overfit: 20 samples of two points from the same flat pattern y = 0.9x + 1.7 + noise.
Left: the least-squares line through each pair swings wildly. Right: Ridge with lambda = 1 on the same pairs
(Plotly). The pattern is the one behind the grey test points of two_points.py."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(0)
xs = np.array([0, 4])
slopes = {0: [], 1: []}
fig = make_subplots(1, 2, horizontal_spacing=0.08, shared_yaxes=True,
                    subplot_titles=("Least squares: through both points", "Ridge, λ = 1"))
for _ in range(20):
    x = rng.uniform(0, 4, 2); y = 0.9 * x + 1.7 + rng.normal(0, 0.5, 2)
    for col, lam in ((1, 0), (2, 1)):
        xc, yc = x - x.mean(), y - y.mean()
        m = (xc @ yc) / (xc @ xc + lam)                      # intercept unpenalised
        b = y.mean() - m * x.mean()
        slopes[lam].append(m)
        fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color="#E45756" if lam == 0 else "#54A24B",
                                 width=2), opacity=0.6), 1, col)
for col in (1, 2):
    fig.add_trace(go.Scatter(x=xs, y=0.9 * xs + 1.7, mode="lines", line=dict(color="black", width=4, dash="dash")), 1, col)
    fig.update_xaxes(title="x", range=[0, 4], row=1, col=col)
s0, s1 = np.array(slopes[0]), np.array(slopes[1])
print(f"slope spread (std): least squares {s0.std():.2f}, ridge {s1.std():.2f}; max |slope| {abs(s0).max():.1f} vs {abs(s1).max():.1f}")
print(f"least-squares slopes {s0.min():.1f} to {s0.max():.1f}, ridge {s1.min():.1f} to {s1.max():.1f}")
assert s1.std() < s0.std()
fig.update_yaxes(title="y", range=[0, 8], row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=20)
fig.write_image(here / "two_point_samples.png", scale=2)
fig.write_image(here / "two_point_samples.pdf")
