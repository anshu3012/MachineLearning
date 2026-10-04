"""How many polynomial features PolynomialFeatures (include_bias=False) makes, by degree and number of original
features (Plotly). Counts come from scikit-learn itself; the 2-feature line matches the Note: 2, 5, 9, 65, 350."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import PolynomialFeatures

here = Path(__file__).parent
degrees = list(range(1, 11))
count = lambda p, d: PolynomialFeatures(degree=d, include_bias=False).fit(np.zeros((1, p))).n_output_features_
assert [count(2, d) for d in (1, 2, 3, 10, 25)] == [2, 5, 9, 65, 350]
COL = {2: "#4C78A8", 5: "#54A24B", 10: "#F58518", 30: "#E45756"}
fig = go.Figure()
for p, c in COL.items():
    n = [count(p, d) for d in degrees]
    fig.add_trace(go.Scatter(x=degrees, y=n, mode="lines+markers", line=dict(color=c, width=4), marker=dict(size=9),
                             name=f"{p} original features"))
    fig.add_annotation(x=10, y=np.log10(n[-1]), text=f"{n[-1]:,}", showarrow=False, xanchor="left", xshift=8,
                       font=dict(color=c, size=20))
    print(p, n)
fig.add_annotation(x=3, y=np.log10(9), text="moons, degree 3: 9", showarrow=True, ax=40, ay=50, font=dict(size=18))
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="degree", tickvals=degrees, range=[0.7, 11.6]),
                  yaxis=dict(title="number of features (log scale)", type="log"),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "feature_count.png", scale=2)
