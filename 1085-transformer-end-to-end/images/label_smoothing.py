"""Section 7.4: plain (one-hot) cross-entropy against label-smoothed cross-entropy (epsilon 0.1, K = 4 words), as the
probability given to the correct word "nous" goes from 0.30 to 0.9999, the rest shared evenly by the other 3 words.
The one-hot loss keeps falling towards certainty; the smoothed loss is lowest at 0.925 and rises again.
Run: python label_smoothing.py  -> label_smoothing.png (Plotly: two loss curves)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, GREY, ORANGE

HERE = Path(__file__).parent
K, eps = 4, 0.1
q = np.full(K, eps / K); q[0] += 1 - eps                    # [0.925, 0.025, 0.025, 0.025]
onehot = lambda p: -np.log(p[0])
smooth = lambda p: -(q * np.log(p)).sum()
spread = lambda a: np.r_[a, np.full(K - 1, (1 - a) / (K - 1))]
u = np.array([2.0, 1.0, 0.5, -1.0]); p_logits = np.exp(u) / np.exp(u).sum()
assert np.allclose(q, [0.925, 0.025, 0.025, 0.025])
assert [round(onehot(p_logits), 3), round(smooth(p_logits), 3)] == [0.495, 0.633]               # the Note's table
assert [round(onehot(q), 3), round(smooth(q), 3)] == [0.078, 0.349]
over = np.array([0.999] + [0.001 / 3] * 3)                    # as in the Notebook
assert [round(onehot(over), 3), round(smooth(over), 3)] == [0.001, 0.601]
a = np.linspace(0.30, 0.9999, 20000)
L_s = np.array([smooth(spread(x)) for x in a])
assert abs(a[L_s.argmin()] - 0.925) < 1e-3 and round(smooth(spread(0.9999)), 3) == 0.773

fig = go.Figure()
fig.add_trace(go.Scatter(x=a, y=[onehot(spread(x)) for x in a], name="one-hot target", line=dict(color=GREY, width=4)))
fig.add_trace(go.Scatter(x=a, y=L_s, name="smoothed target (ε = 0.1)", line=dict(color=ORANGE, width=4)))
fig.add_trace(go.Scatter(x=[0.925], y=[smooth(q)], mode="markers+text", text=["lowest at 0.925"],
                         textposition="bottom center", marker=dict(size=14, color=ORANGE), showlegend=False))
fig.add_trace(go.Scatter(x=[0.9999], y=[smooth(spread(0.9999))], mode="markers+text", text=["0.773: over-confidence<br>is penalised"],
                         textposition="top left", marker=dict(size=12, color=ORANGE), showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title='probability given to the correct word "nous"', range=[0.28, 1.03]),
                  yaxis=dict(title="loss", range=[0, 1.3]), legend=dict(x=0.45, y=0.98),
                  margin=dict(l=80, r=30, t=30, b=70))

if __name__ == "__main__":
    fig.write_image(HERE / "label_smoothing.png", scale=2)
