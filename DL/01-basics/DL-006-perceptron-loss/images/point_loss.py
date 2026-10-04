"""Loss of one point against s = y f(x): 0-1 loss, perceptron loss and hinge loss (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
s = np.linspace(-3, 3, 601)
fig = go.Figure()
fig.add_vrect(x0=-3, x1=0, fillcolor="#E45756", opacity=0.08, line_width=0)
fig.add_vrect(x0=0, x1=3, fillcolor="#54A24B", opacity=0.08, line_width=0)
fig.add_trace(go.Scatter(x=s, y=np.where(s < 0, 1, 0), mode="lines", name="0-1 loss: 1 per mistake",
                         line=dict(color="#6B6B6B", width=3, dash="dot", shape="hv")))
fig.add_trace(go.Scatter(x=s, y=np.maximum(0, 1 - s), mode="lines", name="hinge loss: max(0, 1 - s)",
                         line=dict(color="#4C78A8", width=3, dash="dash")))
fig.add_trace(go.Scatter(x=s, y=np.maximum(0, -s), mode="lines", name="perceptron loss: max(0, -s)",
                         line=dict(color="#E45756", width=5)))
fig.add_annotation(x=-1.5, y=3.6, text="misclassified (s < 0)", showarrow=False, font=dict(size=19, color="#E45756"))
fig.add_annotation(x=1.5, y=3.6, text="correct side (s > 0)", showarrow=False, font=dict(size=19, color="#54A24B"))
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=18),
                  xaxis=dict(title="s = y f(x)   (label times the point's value in the line's equation)", range=[-3, 3],
                             zeroline=False),
                  yaxis=dict(title="loss of one point", range=[-0.1, 4]),
                  legend=dict(x=0.62, y=0.82, bgcolor="rgba(255,255,255,0.9)"), margin=dict(l=70, r=20, t=30, b=70))
fig.write_image(here / "point_loss.png", scale=2)
fig.write_image(here / "point_loss.pdf")
