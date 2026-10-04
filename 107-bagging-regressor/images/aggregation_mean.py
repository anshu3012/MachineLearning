"""Section 2: aggregation in a bagging regressor is the mean. For three inputs x of the two-bumps data, the 50 bagged
trees of section 3 each return a number (grey dots); the bagging prediction is their mean (blue diamond). (Plotly)"""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import fit  # noqa: E402  same data and models as the app

_, (bag, _) = fit("decision tree", n_estimators=50, max_samples=25, bootstrap=True)
XS = [-1.0, 0.0, 2.0]
fig = go.Figure()
for i, x in enumerate(XS):
    preds = np.array([t.predict([[x]])[0] for t in bag.estimators_])
    mean = preds.mean()
    assert np.isclose(mean, bag.predict([[x]])[0])          # the bagging prediction is exactly the mean
    print(x, round(mean, 3), round(preds.min(), 3), round(preds.max(), 3))
    jit = np.random.default_rng(i).uniform(-0.15, 0.15, len(preds))
    fig.add_trace(go.Scatter(x=preds, y=i + jit, mode="markers", showlegend=i == 0, name="one tree's prediction (50 trees)",
                             marker=dict(color="#BBBBBB", size=10, line=dict(color="#6B6B6B", width=1))))
    fig.add_trace(go.Scatter(x=[mean], y=[i], mode="markers", showlegend=i == 0, name="their mean = bagging prediction",
                             marker=dict(symbol="diamond", size=22, color="#4C78A8", line=dict(color="white", width=1))))
    fig.add_annotation(x=mean, y=i + 0.36, text=f"mean {mean:.2f}", showarrow=False, font=dict(size=21, color="#4C78A8"))
fig.update_yaxes(tickvals=list(range(3)), ticktext=[f"x = {x:g}" for x in XS], range=[-0.5, 2.6])
fig.update_xaxes(title="predicted y")
fig.update_layout(template="simple_white", width=1100, height=500, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=100, r=30, t=70, b=70), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.14))
fig.write_image(HERE / "aggregation_mean.png", scale=2)
fig.write_image(HERE / "aggregation_mean.pdf")
