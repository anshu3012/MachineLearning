"""Filter honesty over 500 simulated runs. Left: average NEES (needs the truth); right: average NIS (needs only the
readings). A filter with the right noises stays inside the band where 95 percent of averages of 500 chi-square(1)
values fall; one that assumes the sensor twice as precise (R = 0.0025) sits near 3; one with too little process
noise (Q = 0.0001) drifts upwards. Run: python consistency.py -> consistency.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2
from gifkit import BLUE, FONT, GREEN, RED
from ekfsim import consistency

here = Path(__file__).parent
N = 500
lo, hi = chi2.ppf([0.025, 0.975], N) / N
t = np.arange(1, 17)
fig = make_subplots(rows=1, cols=2, subplot_titles=["average NEES (truth known)", "average NIS (readings only)"],
                    horizontal_spacing=0.1)
for q, r, c, name in ((0.01, 0.01, BLUE, "right noises (Q 0.01, R 0.01)"),
                      (0.01, 0.0025, RED, "sensor trusted too much (R 0.0025)"),
                      (0.0001, 0.01, GREEN, "motion trusted too much (Q 0.0001)")):
    nees, nis = consistency(q, r, N)
    print(name, "NEES", nees.round(2), "NIS", nis.round(2))
    fig.add_trace(go.Scatter(x=t, y=nees, mode="lines+markers", line=dict(color=c, width=3), name=name), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=nis, mode="lines+markers", line=dict(color=c, width=3), showlegend=False), row=1, col=2)
for col in (1, 2):
    fig.add_hrect(y0=lo, y1=hi, fillcolor="grey", opacity=0.25, line_width=0, row=1, col=col)
fig.update_yaxes(type="log", range=[np.log10(0.5), np.log10(40)], tickvals=[0.5, 1, 2, 5, 10, 20, 40], title="average (log scale)", row=1, col=1)
fig.update_yaxes(type="log", range=[np.log10(0.5), np.log10(40)], tickvals=[0.5, 1, 2, 5, 10, 20, 40], row=1, col=2)
fig.update_xaxes(title="step", dtick=3)
fig.update_layout(template="simple_white", font=FONT, width=1250, height=560, margin=dict(l=90, r=30, t=120, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12, yanchor="bottom", font=dict(size=16)))
fig.update_annotations(selector=dict(yref="paper"), font_size=19)
print("band", lo.round(3), hi.round(3))
fig.write_image(here / "consistency.png")
