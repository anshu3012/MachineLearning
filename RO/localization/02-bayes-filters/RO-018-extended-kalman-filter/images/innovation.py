"""The innovations of one run (y = reading minus predicted reading) with the band of two standard deviations the
filter itself predicts (2 sqrt(S)). With the right R about 95 percent of them fall inside; a filter that assumes
R = 0.0025 predicts a band half as wide, and many fall outside. Run: python innovation.py -> innovation.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, RED
from ekfsim import ekf, simulate

here = Path(__file__).parent
xs, zs = simulate(0, T=60)
t = np.arange(1, 61)
fig = make_subplots(rows=1, cols=2, subplot_titles=["filter assumes R = 0.01 (right)", "filter assumes R = 0.0025 (too small)"],
                    horizontal_spacing=0.08, shared_yaxes=True)
for col, r, c in ((1, 0.01, BLUE), (2, 0.0025, RED)):
    rows = ekf(zs, r=r)
    y = np.array([q["y"] for q in rows]); band = 2 * np.sqrt([q["S"] for q in rows])
    out = np.mean(np.abs(y) > band)
    print(r, "share outside", round(out, 3))
    fig.add_trace(go.Scatter(x=np.r_[t, t[::-1]], y=np.r_[band, -band[::-1]], fill="toself", fillcolor="rgba(120,120,120,0.2)",
                             line=dict(width=0)), row=1, col=col)
    fig.add_trace(go.Scatter(x=t, y=y, mode="markers", marker=dict(color=c, size=8)), row=1, col=col)
    fig.add_annotation(x=30, y=0.42, text=f"{100 * out:.0f} percent outside the band", showarrow=False,
                       font=dict(size=18, color=c), row=1, col=col)
fig.update_yaxes(title="innovation (m)", range=[-0.5, 0.5], row=1, col=1)
fig.update_xaxes(title="step")
fig.update_layout(template="simple_white", font=FONT, width=1250, height=520, showlegend=False,
                  margin=dict(l=90, r=30, t=70, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=19)
fig.write_image(here / "innovation.png")
