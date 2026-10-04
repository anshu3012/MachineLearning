"""The missing-trend cause of autocorrelation, from the Notebook's test (Plotly). Data y = 2x + 3 sin(t/25) + noise,
with t the observation number. Left: residuals of a model on x alone, in row order: a slow wave, Durbin-Watson 0.40.
Right: after adding the slow input sin(t/25) as a feature, the residuals jump randomly, Durbin-Watson 2.09."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from statsmodels.stats.stattools import durbin_watson
from gifkit import BLUE, FONT, GREEN, RED

here = Path(__file__).parent
rng = np.random.default_rng(0); t = np.arange(200)
x = rng.normal(size=200); slow = np.sin(t / 25)
y_t = 2 * x + 3 * slow + rng.normal(size=200)
cases = [("model on x alone", x[:, None], RED, 0.40), ("with the slow input added", np.c_[x, slow], GREEN, 2.09)]
fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.06,
                    subplot_titles=[f"{n}: Durbin-Watson {d:.2f}" for n, _, _, d in cases])
fig.update_annotations(font_size=22)
for col, (n, Xt, c, d) in enumerate(cases, 1):
    r = y_t - LinearRegression().fit(Xt, y_t).predict(Xt)
    assert round(durbin_watson(r), 2) == d
    fig.add_trace(go.Bar(x=t, y=r, marker_color=c, marker_line_width=0), 1, col)
    fig.update_xaxes(title="observation number (row order)", row=1, col=col)
fig.update_yaxes(title="residual", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=480, font=FONT, showlegend=False, bargap=0.1,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "autocorr_fix.png", scale=2)
