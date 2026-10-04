"""The 40 test errors, sorted: absolute values (MAE is their mean) vs squares (MSE is their mean) (Plotly).
Squaring shrinks the small errors and stretches the large ones."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import y, pred, BLUE, ORANGE, RED, FONT

here = Path(__file__).parent
a = np.sort(np.abs(y - pred))
s = a ** 2
mae, mse = a.mean(), s.mean()
top5 = s[-5:].sum() / s.sum()
print(f"MAE {mae:.3f} MSE {mse:.3f}; largest 5 errors give {top5:.0%} of the squared total, {a[-5:].sum() / a.sum():.0%} of the absolute")
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=(
    f"Absolute errors: mean = MAE = {mae:.2f}", f"Squared errors: mean = MSE = {mse:.2f}"))
k = np.arange(1, 41)
for col, v, c, m in ((1, a, BLUE, mae), (2, s, ORANGE, mse)):
    fig.add_trace(go.Bar(x=k, y=v, marker_color=c), 1, col)
    fig.add_trace(go.Scatter(x=[0.5, 40.5], y=[m, m], mode="lines", line=dict(color=RED, width=3, dash="dash")), 1, col)
    fig.update_xaxes(title="test students, smallest error to largest", row=1, col=col)
    fig.update_yaxes(range=[0, 1], row=1, col=col)
fig.add_annotation(x=20, y=0.8, text=f"largest 5 errors:<br>{top5:.0%} of the squared total<br>({a[-5:].sum() / a.sum():.0%} of the absolute total)", showarrow=False,
                   font=dict(size=17, color=ORANGE), row=1, col=2)
fig.update_yaxes(title="error (LPA)", row=1, col=1)
fig.update_yaxes(title="error² (LPA²)", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=17)
fig.write_image(here / "abs_vs_squared.png", scale=2)
fig.write_image(here / "abs_vs_squared.pdf")
