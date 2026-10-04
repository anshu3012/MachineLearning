"""Local maxima (Plotly). EM (scikit-learn GaussianMixture, three full-covariance components, means started at three
random observations, random_state 0-19) on the Iris flowers. Each start is one dot: its final log-likelihood and how well
its clusters match the species (ARI). 9 starts reach the best hilltop, -180.2 with ARI 0.90; the other 11 stop on
lower hilltops (-186.6 to -203.5) with ARI 0.47 to 0.72."""
from collections import Counter
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

from em_core import BLUE, FONT, GREY, RED

HERE = Path(__file__).parent
Xi, yi = load_iris(return_X_y=True)
finals = []
for s in range(20):
    g = GaussianMixture(3, covariance_type="full", init_params="random_from_data",
                        random_state=s, max_iter=1000, tol=1e-6).fit(Xi)
    finals.append((round(g.score(Xi) * len(Xi), 1), round(adjusted_rand_score(yi, g.predict(Xi)), 2)))
ll = np.array([f[0] for f in finals]); ari = np.array([f[1] for f in finals])
best = ll == ll.max()
assert ll.max() == -180.2 and ari[best].min() == 0.90 and best.sum() == 9
assert ll[~best].max() == -186.6 and ll.min() == -203.5 and ari[~best].min() == 0.47 and ari[~best].max() == 0.72

cnt = Counter(finals)
fig = go.Figure()
for (l, a), n in cnt.items():
    col = RED if l == ll.max() else BLUE
    fig.add_trace(go.Scatter(x=[l], y=[a], mode="markers+text", marker=dict(size=14 + 5 * n, color=col, opacity=0.85),
                             text=[f"{n} starts" if n > 1 else ""], textposition="bottom center" if n < 9 else "middle left",
                             textfont=dict(size=19, color=col)))
fig.add_annotation(x=-180.2, y=0.90, text="best hilltop −180.2, ARI 0.90", showarrow=False, yshift=40, xanchor="right",
                   font=dict(size=20, color=RED))
fig.add_annotation(x=-195, y=0.8, text="11 starts stop on lower hilltops", showarrow=False, font=dict(size=20, color=BLUE))
fig.update_layout(template="simple_white", width=950, height=560, showlegend=False, font=FONT,
                  xaxis=dict(title="final log-likelihood (higher is better)", range=[-206, -178]),
                  yaxis=dict(title="ARI against the species", range=[0.4, 1.0]),
                  margin=dict(l=80, r=30, t=30, b=60))
fig.write_image(HERE / "iris_starts.png", scale=2)
fig.write_image(HERE / "iris_starts.pdf")
print(sorted(cnt.items(), reverse=True))
