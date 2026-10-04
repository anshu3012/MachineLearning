"""Section 3: the hand-picked 2-number embeddings of the Note as arrows from the origin: money (2, 7), bank (7, 3)
and river (8, -2), with the angle of each arrow. Data: data/vectors.csv (kind e). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import GREY, GREEN, BLUE, ORANGE, FONT

here = Path(__file__).parent
V = pd.read_csv(here.parent / "data" / "vectors.csv").query("kind == 'e'").drop_duplicates("word").set_index("word")
E = {w: V.loc[w, ["x", "y"]].to_numpy(float) for w in ("money", "bank", "river")}
assert E["money"].tolist() == [2, 7] and E["bank"].tolist() == [7, 3] and E["river"].tolist() == [8, -2]
fig = go.Figure()
for w, col in (("money", GREEN), ("bank", GREY), ("river", BLUE)):
    x, y = E[w]
    ang = np.degrees(np.arctan2(y, x))
    fig.add_annotation(x=x, y=y, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2,
                       arrowwidth=4, arrowcolor=col, text="")
    fig.add_annotation(x=x, y=y, text=f"<b>{w}</b> ({x:g}, {y:g}), {ang:.0f}°", showarrow=False, xanchor="left",
                       xshift=10, font=dict(size=20, color=col))
fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(size=8, color="black"), showlegend=False)
fig.update_layout(template="simple_white", width=900, height=640, font=dict(FONT, size=20),
                  xaxis=dict(range=[-1, 14], title="first number", zeroline=True, dtick=2),
                  yaxis=dict(range=[-3, 8], title="second number", zeroline=True, scaleanchor="x", dtick=2),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "word_arrows.png", scale=2)
fig.write_image(here / "word_arrows.pdf")
