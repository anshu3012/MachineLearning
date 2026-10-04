"""Decision surface of KNN (k = 5) on the first two breast cancer columns, with the regions and boundary labelled (Plotly)."""
import sys
from pathlib import Path

import plotly.graph_objects as go

here = Path(__file__).parent
sys.path.insert(0, str(here.parent))
from app import traces, xs, ys          # same data and surface code as the app

data_traces, acc = traces(5)
print("k = 5 on two columns, test accuracy", round(acc, 3))
fig = go.Figure(data_traces)
box = dict(bgcolor="white", bordercolor="#555", borderwidth=1, font=dict(size=17))
fig.add_annotation(x=10.5, y=34, text="benign region", showarrow=False, **box)
fig.add_annotation(x=23, y=12, text="malignant region", showarrow=False, **box)
fig.add_annotation(x=15.5, y=27.5, ax=90, ay=-50, text="decision boundary", arrowwidth=2, arrowcolor="black", **box)
fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=17),
                  xaxis=dict(title="mean radius", range=[xs[0], xs[-1]]), yaxis=dict(title="mean texture", range=[ys[0], ys[-1]]),
                  legend=dict(x=1.01, y=1), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(here / "decision_surface.png", scale=2); fig.write_image(here / "decision_surface.pdf")
