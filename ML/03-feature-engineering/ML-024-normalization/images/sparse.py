"""Why max-abs scaling suits sparse data: the Note's column [0, 0, -4, 0, 2, 0, 8] after max-abs scaling keeps its
four zeros at exactly 0, while min-max scaling turns every zero into 0.333."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler

here = Path(__file__).parent
s = np.array([[0], [0], [-4], [0], [2], [0], [8.0]])
ma, mm = MaxAbsScaler().fit_transform(s).ravel(), MinMaxScaler().fit_transform(s).ravel()
assert list(ma) == [0, 0, -0.5, 0, 0.25, 0, 1] and np.allclose(mm[[0, 1, 3, 5]], 1 / 3)
cols = [("original", s.ravel(), "4 zeros of 7"), ("max-abs: divide by 8", ma, "zeros stay 0"),
        ("min-max", mm, "zeros become 0.333")]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06, subplot_titles=[f"{a}<br><b>{c}</b>" for a, _, c in cols])
for j, (_, v, _) in enumerate(cols, start=1):
    z = v.reshape(-1, 1)
    fig.add_heatmap(z=z, x=[""], y=[f"row {i + 1}" for i in range(7)], showscale=False, colorscale="RdBu", zmid=0,
                    zmin=-8 if j == 1 else -1, zmax=8 if j == 1 else 1, xgap=3, ygap=3, row=1, col=j)
    for i, x in enumerate(v):
        fig.add_annotation(x=0, y=i, text=f"{x:.3g}", showarrow=False, font=dict(size=22, color="black"),
                           xref=f"x{j if j > 1 else ''}", yref=f"y{j if j > 1 else ''}")
fig.update_yaxes(autorange="reversed", showticklabels=False)
fig.update_annotations(selector=dict(xref="paper"), font_size=20)
fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=20, r=20, t=100, b=20))
fig.write_image(here / "sparse.png", scale=2)
fig.write_image(here / "sparse.pdf")
