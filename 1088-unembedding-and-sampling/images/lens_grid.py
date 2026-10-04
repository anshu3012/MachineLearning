"""Logit lens grid (after nostalgebraist 2020): the top next-token guess at every position (columns) after every
block (rows), GPT-2 small on "Steve Jobs was the founder of". Colour = probability of that guess; outlined
cells already match the final guess. Data: data/logit_lens_grid.csv (Notebook).
Run: python lens_grid.py -> lens_grid.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import FONT, ORANGE, DATA

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "logit_lens_grid.csv", keep_default_na=False)
cols = d[d.layer == 0].sort_values("position").input.str.strip().tolist()
P = d.pivot(index="layer", columns="position", values="prob").values
G = d.pivot(index="layer", columns="position", values="guess").map(lambda t: t.strip() or repr(t)).values
F = d.pivot(index="layer", columns="position", values="final_guess").map(lambda t: t.strip() or repr(t)).values
rows = ["embedding"] + [f"block {l}" for l in range(1, 13)]
fig = go.Figure(go.Heatmap(z=P, x=[f"{c}<br>→ ?" for c in cols], y=rows, colorscale=[[0, "white"], [1, "#6BAED6"]], zmin=0, zmax=1,
                           text=G, texttemplate="%{text}", textfont=dict(size=17, color="black"),
                           colorbar=dict(title="probability", len=0.8)))
for l in range(13):
    for i in range(len(cols)):
        if G[l, i] == F[l, i]:
            fig.add_shape(type="rect", x0=i - 0.48, x1=i + 0.48, y0=l - 0.46, y1=l + 0.46, line=dict(color=ORANGE, width=3), fillcolor="rgba(0,0,0,0)", opacity=1)
fig.update_layout(template="simple_white", width=900, height=760, font=FONT,
                  yaxis=dict(autorange="reversed", title="read after"), xaxis=dict(side="top", title="input token"),
                  margin=dict(l=110, r=20, t=110, b=20))
fig.write_image(HERE / "lens_grid.png", scale=2)
