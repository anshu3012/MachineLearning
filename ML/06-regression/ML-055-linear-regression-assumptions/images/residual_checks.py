"""Assumptions 3-5 on the 60 test residuals: distribution, Q-Q plot, residuals vs prediction, residuals in order (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from common import residual, y_pred, BLUE, ORANGE, RED, GREY, FONT

here = Path(__file__).parent
(osm, osr), (slope, inter, _) = stats.probplot(residual)
kde = stats.gaussian_kde(residual)
xs = np.linspace(residual.min() - 10, residual.max() + 10, 200)
fig = make_subplots(2, 2, vertical_spacing=0.16, horizontal_spacing=0.1, subplot_titles=(
    "3. Normality: distribution of residuals", "3. Normality: Q-Q plot",
    "4. Homoscedasticity: residual vs prediction", "5. No autocorrelation: residuals in order"))
fig.add_trace(go.Histogram(x=residual, histnorm="probability density", nbinsx=15, marker_color=BLUE, opacity=0.5), 1, 1)
fig.add_trace(go.Scatter(x=xs, y=kde(xs), mode="lines", line=dict(color=BLUE, width=3)), 1, 1)
fig.add_trace(go.Scatter(x=osm, y=osr, mode="markers", marker=dict(size=7, color=BLUE)), 1, 2)
fig.add_trace(go.Scatter(x=osm, y=slope * osm + inter, mode="lines", line=dict(color=RED, width=2)), 1, 2)
fig.add_trace(go.Scatter(x=y_pred, y=residual, mode="markers", marker=dict(size=7, color=BLUE)), 2, 1)
fig.add_trace(go.Scatter(x=[y_pred.min(), y_pred.max()], y=[0, 0], mode="lines", line=dict(color=GREY, dash="dash")), 2, 1)
fig.add_trace(go.Scatter(x=np.arange(len(residual)), y=residual, mode="lines+markers", line=dict(color=BLUE, width=1.5),
                         marker=dict(size=5)), 2, 2)
fig.update_xaxes(title="residual", row=1, col=1); fig.update_xaxes(title="normal quantile", row=1, col=2)
fig.update_xaxes(title="predicted target", row=2, col=1); fig.update_xaxes(title="test row", row=2, col=2)
fig.update_yaxes(title="residual", row=2, col=1); fig.update_yaxes(title="residual", row=2, col=2)
fig.update_yaxes(title="sorted residual", row=1, col=2)
fig.update_layout(template="simple_white", width=1050, height=760, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
print("skew", round(stats.skew(residual), 3), "shapiro p", round(stats.shapiro(residual).pvalue, 3))
fig.write_image(here / "residual_checks.png", scale=2)
fig.write_image(here / "residual_checks.pdf")
