"""Recommending by distance: B's bag-of-words vector against A's and C's. Every word in one text but not the other
adds 1 to the sum of squares, so d(B, C) = sqrt(5) and d(A, B) = sqrt(8): C is the nearest, so C is recommended.
Run: python bow_distance.py  -> bow_distance.png/.pdf (Plotly)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
vocab = ["hi", "how", "are", "you", "my", "name", "is", "riya", "this", "2023"]
texts = {"A": "hi how are you", "B": "my name is riya", "C": "this is 2023"}
vec = {k: np.array([t.split().count(w) for w in vocab]) for k, t in texts.items()}
dist = {k: np.sqrt(((vec["B"] - vec[k]) ** 2).sum()) for k in "AC"}
assert np.isclose(dist["C"], np.sqrt(5)) and np.isclose(dist["A"], np.sqrt(8))   # the Note's numbers
assert dist["C"] < dist["A"]

fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2,
                    subplot_titles=[f"B vs C: 5 words differ, d = sqrt(5) = {dist['C']:.2f}  (nearest: recommend C)",
                                    f"B vs A: 8 words differ, d = sqrt(8) = {dist['A']:.2f}"])
for r, k in enumerate("CA", start=1):
    sq = (vec["B"] - vec[k]) ** 2
    z = np.vstack([vec["B"], vec[k], sq])
    fig.add_trace(go.Heatmap(z=z, x=vocab, y=["B", k, "(diff)²"], text=z, texttemplate="%{text}",
                             colorscale=[[0, "white"], [1, BLUE if r == 1 else GREY]], zmin=0, zmax=1.4,
                             showscale=False, xgap=3, ygap=3, textfont=dict(size=20)), row=r, col=1)
    fig.update_yaxes(autorange="reversed", row=r, col=1)
fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Which movie is closest to B?", x=0.5), margin=dict(l=90, r=20, t=110, b=30))
fig.update_annotations(font_size=20)
fig.write_image(HERE / "bow_distance.png", scale=2)
fig.write_image(HERE / "bow_distance.pdf")
