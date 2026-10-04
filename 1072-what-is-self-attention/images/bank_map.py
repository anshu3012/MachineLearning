"""2-D map (PCA) of real word vectors: static 'bank' sits with the money words; self-attention moves it (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
m = pd.read_csv(here.parent / "data" / "bank_map.csv")
fig = go.Figure()
style = {"money": (GREEN, "circle", 13, "money words"), "river": (BLUE, "circle", 13, "river words"),
         "static": (GREY, "square", 18, "static 'bank' (every sentence)"),
         "contextual": (RED, "diamond", 18, "'bank' after self-attention")}
pos = {"money": "top center", "cash": "bottom center", "loan": "bottom center", "account": "top left", "grows": "middle right",
       "river": "top center", "lake": "bottom center", "boat": "top center", "flows": "top center", "bridge": "bottom center",
       "bank": "top center", "bank in 'money bank grows'": "bottom center", "bank in 'river bank flows'": "top center"}
for kind, (c, sym, size, name) in style.items():
    d = m[m.kind == kind]
    fig.add_trace(go.Scatter(x=d.x, y=d.y, mode="markers+text", text=d.label, textposition=[pos[l] for l in d.label],
                             marker=dict(color=c, symbol=sym, size=size), name=name, textfont=dict(size=15, color=c)))
s = m.set_index("label")
for lab in ("bank in 'money bank grows'", "bank in 'river bank flows'"):
    fig.add_annotation(x=s.loc[lab, "x"], y=s.loc[lab, "y"], ax=s.loc["bank", "x"], ay=s.loc["bank", "y"], xref="x", yref="y",
                       axref="x", ayref="y", showarrow=True, arrowhead=3, arrowwidth=2.5, arrowcolor=RED, standoff=10, startstandoff=10)
fig.update_layout(template="simple_white", width=950, height=560, font=FONT,
                  xaxis=dict(title="direction 1", range=[-0.95, 0.95], showticklabels=False),
                  yaxis=dict(title="direction 2", range=[-1.15, 0.45], showticklabels=False),
                  legend=dict(x=0.01, y=0.02, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=60, r=20, t=20, b=60))
fig.write_image(here / "bank_map.png", scale=2)
fig.write_image(here / "bank_map.pdf")
