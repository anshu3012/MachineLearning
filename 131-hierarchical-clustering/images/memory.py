"""Section 11: memory needed for the full n x n proximity matrix at 8 bytes per distance, against the number of points
n, with 16 GB of RAM marked. 10^6 points need 8 TB. Plotly, log scales."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
n = np.logspace(2, 6, 60)
b = 8 * n ** 2
assert 8 * (10 ** 6) ** 2 == 8e12                      # 8 terabytes, the Note's number
fig = go.Figure(go.Scatter(x=n, y=b, mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False))
fig.add_hline(y=16e9, line=dict(color="#E45756", dash="dash", width=2), opacity=1)
fig.add_annotation(x=2.3, y=np.log10(16e9), text="16 GB of RAM", showarrow=False, yshift=14, font=dict(size=17, color="#E45756"))
for x, label in ((200, "200 customers (section 10):<br>320 KB"), (1e6, "10<sup>6</sup> points: 8 TB")):
    fig.add_scatter(x=[x], y=[8 * x * x], mode="markers", marker=dict(size=12, color="black"), showlegend=False)
    fig.add_annotation(x=np.log10(x), y=np.log10(8 * x * x), text=label, showarrow=True, ax=150 if x < 1e3 else -70, ay=-70 if x < 1e3 else 60,
                       font=dict(size=16))
fig.update_layout(template="simple_white", width=1000, height=440, font=FONT,
                  xaxis=dict(type="log", title="number of points n", exponentformat="power", dtick=1),
                  yaxis=dict(type="log", title="bytes for the n × n matrix", exponentformat="power", dtick=2),
                  margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "memory.png", scale=2)
fig.write_image(here / "memory.pdf")
