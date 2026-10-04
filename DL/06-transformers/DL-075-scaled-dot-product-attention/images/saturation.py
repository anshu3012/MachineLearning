"""Left: variance of q.k against d, before and after scaling. Middle: mean largest softmax weight (10 keys).
Right: mean size of the softmax Jacobian, the gradient that passes back through the softmax (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREEN, GREY, FONT

here = Path(__file__).parent
v = pd.read_csv(here.parent / "data" / "variance_vs_d.csv")
s = pd.read_csv(here.parent / "data" / "saturation.csv")
fig = make_subplots(1, 3, subplot_titles=["variance of the scores", "largest softmax weight",
                                          "size of the softmax gradient"], horizontal_spacing=0.09)
for name, col, c in (("without scaling", "var_dot", GREY), ("divided by √d", "var_scaled", GREEN)):
    fig.add_trace(go.Scatter(x=v.d, y=v[col], name=name, mode="lines+markers", line=dict(color=c, width=3)), 1, 1)
for k, col in ((2, "max_weight"), (3, "jacobian_norm")):
    for ver, c in (("unscaled", GREY), ("scaled", GREEN)):
        t = s[s.version == ver]
        fig.add_trace(go.Scatter(x=t.d, y=t[col], showlegend=False, mode="lines+markers",
                                 line=dict(color=c, width=3)), 1, k)
fig.update_xaxes(type="log", title_text="dimension d", dtick=1)
fig.update_yaxes(type="log", row=1, col=1)
fig.update_yaxes(range=[0, 1.02], row=1, col=2)
fig.update_yaxes(range=[0, 0.4], row=1, col=3)
fig.update_layout(template="simple_white", width=1150, height=420, font=FONT,
                  legend=dict(x=0.0, y=1.0), margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "saturation.png", scale=2)
fig.write_image(here / "saturation.pdf")
