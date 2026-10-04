"""Adding useless random columns: R2 creeps up on the training set; adjusted R2 does not; on the test set both fall
(Plotly). Averaged over 200 draws of the random columns, same split as the Notebook."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from common import df, BLUE, ORANGE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
adj = lambda r2, n, k: 1 - (1 - r2) * (n - 1) / (n - 1 - k)
ks, S = list(range(0, 21)), 200
rows = np.zeros((len(ks), 4))
for seed in range(S):
    noise = np.random.default_rng(seed).random((len(df), 20))
    Xtr0, Xte0, ytr, yte = train_test_split(np.c_[df.cgpa.to_numpy(), noise], df.package.to_numpy(),
                                            test_size=0.2, random_state=2)
    for k in ks:
        m = LinearRegression().fit(Xtr0[:, :1 + k], ytr)
        r_tr, r_te = r2_score(ytr, m.predict(Xtr0[:, :1 + k])), r2_score(yte, m.predict(Xte0[:, :1 + k]))
        rows[k] += (r_tr, adj(r_tr, len(ytr), 1 + k), r_te, adj(r_te, len(yte), 1 + k))
rows = rows / S
fig = go.Figure()
for i, (name, colour, dash) in enumerate((("R² training", BLUE, None), ("adjusted R² training", BLUE, "dash"),
                                          ("R² test", ORANGE, None), ("adjusted R² test", ORANGE, "dash"))):
    fig.add_trace(go.Scatter(x=ks, y=rows[:, i], mode="lines+markers", name=name,
                             line=dict(color=colour, width=3, dash=dash), marker=dict(size=6)))
fig.update_layout(template="simple_white", width=950, height=500, font=FONT, legend=dict(x=0.02, y=0.05),
                  title=dict(text="CGPA plus k columns of random numbers (average of 200 draws)", x=0.5),
                  xaxis=dict(title="Number of useless random columns added (k)"),
                  yaxis=dict(title="Score", range=[0.45, 0.85]), margin=dict(l=70, r=30, t=60, b=60))
for k in (0, 1, 5, 10, 20):
    print(k, rows[k].round(4))
fig.write_image(here / "adjusted_r2.png", scale=2)
fig.write_image(here / "adjusted_r2.pdf")
