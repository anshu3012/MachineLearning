"""Breast cancer data, standardised: 5-fold CV accuracy and number of non-zero coefficients against C, for L2 and L1 (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.simplefilter("ignore")

here = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
Cs = np.logspace(-3, 2, 16)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Cross-validated accuracy", "Coefficients that are not zero (of 30)"))
for l1, name, col in ((0, "L2 (l1_ratio = 0)", "#4C78A8"), (1, "L1 (l1_ratio = 1)", "#E45756")):
    acc, nz = [], []
    for C in Cs:
        m = make_pipeline(StandardScaler(), LogisticRegression(C=C, l1_ratio=l1, solver="saga", max_iter=50000))
        acc.append(cross_val_score(m, X, y, cv=5).mean())
        nz.append(int((np.abs(m.fit(X, y)[-1].coef_) > 1e-8).sum()))
    print(name, [round(a, 3) for a in acc], nz)
    fig.add_trace(go.Scatter(x=Cs, y=acc, mode="lines+markers", line=dict(color=col, width=3), name=name), 1, 1)
    fig.add_trace(go.Scatter(x=Cs, y=nz, mode="lines+markers", line=dict(color=col, width=3), showlegend=False), 1, 2)
fig.add_annotation(x=np.log10(0.002), y=0.66, text="strong penalty:<br>underfits", showarrow=False, font=dict(size=13, color="#555"), row=1, col=1)
fig.add_annotation(x=np.log10(50), y=0.93, text="weak penalty:<br>slight overfitting", showarrow=False, font=dict(size=13, color="#555"), row=1, col=1)
fig.update_xaxes(type="log", title="C  (smaller C = stronger regularisation)", exponentformat="power", dtick=1)
fig.update_yaxes(range=[0.6, 1.0], title="accuracy", row=1, col=1)
fig.update_yaxes(range=[-1, 31], title="count", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=480, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.25, y=0.15), margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "c_path.png", scale=2); fig.write_image(here / "c_path.pdf")
