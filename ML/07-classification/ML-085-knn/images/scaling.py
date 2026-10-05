"""Why KNN needs scaling, on the breast cancer training set (Plotly). Left: the standard deviation of each of the 30
features on a log scale, raw and after StandardScaler; raw spreads range from about 0.002 to over 500, so the
large-number features dominate every distance. Right: test accuracy with k = 5, raw 0.912 (104 of 114) and scaled
0.974 (111 of 114)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)
sc = StandardScaler().fit(Xtr)
raw = KNeighborsClassifier(5).fit(Xtr, ytr).score(Xte, yte)
scl = KNeighborsClassifier(5).fit(sc.transform(Xtr), ytr).score(sc.transform(Xte), yte)
assert (round(raw, 3), round(scl, 3)) == (0.912, 0.974)
sd = Xtr.std(0)
order = np.argsort(sd)[::-1]
names = np.array(load_breast_cancer().feature_names)[order]
fig = make_subplots(1, 2, column_widths=[0.7, 0.3], horizontal_spacing=0.1,
                    subplot_titles=["spread of each feature (standard deviation)", "test accuracy, k = 5"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Bar(x=list(range(30)), y=sd[order], marker_color=ORANGE, name="raw features", hovertext=names), 1, 1)
fig.add_trace(go.Scatter(x=list(range(30)), y=np.ones(30), mode="lines", line=dict(color=BLUE, width=4), name="after standardization (all 1)"), 1, 1)
fig.add_annotation(x=0, y=np.log10(sd[order][0]), text=names[0], showarrow=False, xanchor="left", yshift=14, font=dict(size=16), row=1, col=1)
fig.add_trace(go.Bar(x=["raw", "scaled"], y=[raw, scl], marker_color=[ORANGE, BLUE], text=[f"{raw:.3f}", f"{scl:.3f}"],
                     textposition="outside", textfont=dict(size=20), showlegend=False), 1, 2)
fig.update_xaxes(title="the 30 features, largest spread first", showticklabels=False, row=1, col=1)
TICKS = [0.001, 0.01, 0.1, 1, 10, 100, 1000]   # one labelled gridline per power of ten, no minor labels
fig.update_yaxes(type="log", tickvals=TICKS, ticktext=[f"{t:g}" for t in TICKS], showgrid=True,
                 title="standard deviation (log scale)", row=1, col=1)
fig.update_yaxes(range=[0.8, 1.02], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=540, font=FONT,
                  legend=dict(orientation="h", x=0.35, xanchor="center", y=-0.18), margin=dict(l=80, r=30, t=60, b=120))
fig.write_image(here / "scaling.png", scale=2)
assert sd.min() < 0.003 and sd.max() > 500 and names[0] == "worst area"
