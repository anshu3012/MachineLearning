"""Winning top-5 error of the ImageNet challenge (ILSVRC) by year, with the human estimate (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, FONT

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "ilsvrc_winners.csv")
w["label"] = [f"{e:g}%<br>{n.replace('SuperVision (AlexNet)', 'AlexNet')}" for e, n in zip(w.top5_error, w.entry)]
fig = go.Figure()
for kind, name, c in (("hand-made features", "hand-made features + classic ML", GREY), ("CNN", "CNN", BLUE)):
    d = w[w.kind == kind]
    fig.add_trace(go.Bar(x=d.year, y=d.top5_error, name=name, marker_color=c, width=0.6, text=d.label,
                         textposition="outside", textfont=dict(size=16), cliponaxis=False))
fig.add_trace(go.Scatter(x=[2009.6, 2015.4], y=[5.1, 5.1], mode="lines", name="one trained human (5.1%)",
                         line=dict(color=RED, width=2, dash="dash")))
fig.update_layout(template="simple_white", width=950, height=480, font=FONT, uniformtext=dict(minsize=14, mode="show"),
                  xaxis=dict(title="year", tickmode="array", tickvals=list(w.year), range=[2009.5, 2015.5]),
                  yaxis=dict(title="top-5 error of the winner (%)", range=[0, 36]),
                  legend=dict(x=0.62, y=0.98, bgcolor="rgba(255,255,255,0.9)"), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(here / "ilsvrc_errors.png", scale=2)
fig.write_image(here / "ilsvrc_errors.pdf")
