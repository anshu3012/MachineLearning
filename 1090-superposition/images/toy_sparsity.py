"""Toy model of superposition (Elhage et al. 2022): the 2-number direction W_i of each of 5 features after
training, as the features get sparser. Importance falls 0.7^i (feature 1 most important). Last panel: the same
data at S = 0.95 but with no ReLU. Data: data/toy_models.csv (Notebook). Run: python toy_sparsity.py"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

HERE = Path(__file__).parent
t = pd.read_csv(HERE.parent / "data" / "toy_models.csv")
SHADES = ["#B2182B", "#EF8A62", "#4C78A8", "#54A24B", "#B279A2"]
panels = [("ReLU", 0.0), ("ReLU", 0.7), ("ReLU", 0.9), ("ReLU", 0.95), ("linear", 0.95)]
titles = []
for m, S in panels:
    d = t[(t.model == m) & (t.importance == "0.7^i") & (t.S == S)]
    titles.append(f"{'ReLU' if m == 'ReLU' else 'no ReLU'}, S = {S}<br><b>{(d.norm > 0.5).sum()} of 5 stored</b>")
fig = make_subplots(rows=1, cols=5, subplot_titles=titles, horizontal_spacing=0.03)
for k, (m, S) in enumerate(panels, 1):
    d = t[(t.model == m) & (t.importance == "0.7^i") & (t.S == S)]
    for _, r in d.iterrows():
        i = int(r.feature) - 1
        fig.add_trace(go.Scatter(x=[0, r.w1], y=[0, r.w2], mode="lines+markers", line=dict(color=SHADES[i], width=5),
                                 marker=dict(size=[0, 13], color=SHADES[i]), name=f"feature {i + 1}",
                                 showlegend=(k == 4)), row=1, col=k)
    fig.update_xaxes(range=[-1.35, 1.35], showticklabels=False, zeroline=True, row=1, col=k)
    fig.update_yaxes(range=[-1.35, 1.35], showticklabels=False, zeroline=True, scaleanchor=f"x{k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1500, height=440, font=dict(FONT, size=17),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08, title_text="most to least important:"),
                  margin=dict(l=20, r=20, t=90, b=60))
fig.write_image(HERE / "toy_sparsity.png", scale=2)
fig.write_image(HERE / "toy_sparsity.pdf")
