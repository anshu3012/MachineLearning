"""Sections 4.2 and 5.1: the same decoder state s and four encoder states h_1..h_4, scored three ways (Bahdanau's
additive network, Luong dot, Luong general), and the softmax weights each gives. Random numbers, seeded exactly as in
the Notebook, so the values are the Note's worked examples.
Run: python three_scores.py  -> three_scores.png (Plotly: scores and weights side by side)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN, ORANGE

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
Hs = rng.uniform(-1, 1, (4, 4)).round(1)
s = np.array([0.5, -0.2, 0.8, 0.1])
softmax = lambda z: np.exp(z - z.max()) / np.exp(z - z.max()).sum()
W, v = rng.uniform(-1, 1, (8, 3)).round(1), rng.uniform(-1, 1, (3,)).round(1)
e_add = np.tanh(np.hstack([np.tile(s, (4, 1)), Hs]) @ W) @ v
e_dot = Hs @ s
Wa = rng.uniform(-1, 1, (4, 4)).round(1)
e_gen = Hs @ (Wa.T @ s)
scores = {"Bahdanau (additive)": (e_add, ORANGE), "Luong dot": (e_dot, BLUE), "Luong general": (e_gen, GREEN)}
assert list(Hs[0]) == [0.3, -0.5, -0.9, -1.0] and list(v) == [0.1, -0.4, 0.2]
assert np.allclose(e_add.round(3), [-0.099, -0.011, 0.449, -0.116]) and np.allclose(softmax(e_add).round(3), [0.208, 0.227, 0.360, 0.205])
assert np.allclose(e_dot.round(2), [-0.57, 0.35, 0.25, 0.87]) and np.allclose(softmax(e_dot).round(3), [0.100, 0.251, 0.227, 0.422])
assert np.allclose(e_gen.round(3), [0.477, -0.254, 0.975, -0.887]) and np.allclose(softmax(e_gen).round(3), [0.296, 0.142, 0.486, 0.076])

x = ["h<sub>1</sub>", "h<sub>2</sub>", "h<sub>3</sub>", "h<sub>4</sub>"]
fig = make_subplots(1, 2, subplot_titles=["scores e<sub>j</sub>", "weights α<sub>j</sub> = softmax(e)"], horizontal_spacing=0.1)
for name, (e, c) in scores.items():
    fig.add_trace(go.Bar(x=x, y=e, name=name, marker_color=c, text=[f"{z:.2f}" for z in e], textposition="outside"), 1, 1)
    a = softmax(e)
    fig.add_trace(go.Bar(x=x, y=a, name=name, marker_color=c, text=[f"{z:.2f}" for z in a], textposition="outside",
                         showlegend=False), 1, 2)
fig.update_yaxes(range=[-1.15, 1.25], zeroline=True, zerolinecolor="#6B6B6B", row=1, col=1)
fig.update_yaxes(range=[0, 0.62], row=1, col=2)
fig.update_layout(template="simple_white", barmode="group", width=1200, height=540, bargap=0.25,
                  font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12, yanchor="bottom"),
                  margin=dict(l=60, r=20, t=120, b=40))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "three_scores.png", scale=2)
