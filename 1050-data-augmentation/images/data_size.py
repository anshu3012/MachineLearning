"""Augmentation stretches a small dataset, from data/data_size.json (experiments/data_size.py: the Note's model with
and without its three random layers, 500 to 2,000 training photos, 60 epochs, 4 seeds, GPU; test accuracy on the
same 1,000 photos). Dots: single runs; lines: their means. Plotly."""
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
R = json.load(open(HERE.parent / "data" / "data_size.json"))
N = [500, 1000, 2000]
P = np.array([R[f"{n}_plain"] for n in N]) * 100
A = np.array([R[f"{n}_aug"] for n in N]) * 100
assert (A.mean(1) > P.mean(1)).all() and A.mean(1)[1] > P.mean(1)[2]
X = np.arange(3)
fig = go.Figure()
for M, col, name, off in ((P, "#4C78A8", "without augmentation", -0.06), (A, "#54A24B", "with augmentation", 0.06)):
    for k in range(M.shape[1]):
        fig.add_scatter(x=X + off, y=M[:, k], mode="markers", marker=dict(size=9, color=col, opacity=0.4),
                        showlegend=False)
    fig.add_scatter(x=X + off, y=M.mean(1), mode="lines+markers+text", text=[f"{v:.1f}%" for v in M.mean(1)],
                    textposition="top center" if off > 0 else "bottom center", textfont=dict(size=18, color=col),
                    line=dict(color=col, width=4), marker=dict(size=13), name=name)
fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Test accuracy on 1,000 photos after 60 epochs (4 runs per point)", x=0.5,
                             font=dict(size=21)),
                  xaxis=dict(title="training photos (half cats, half dogs)", tickvals=X, ticktext=["500", "1,000", "2,000"],
                             range=[-0.4, 2.4]),
                  yaxis=dict(title="test accuracy (%)", range=[57, 85]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=30, t=70, b=80))
fig.write_image(HERE / "data_size.png", scale=2)
print(P.mean(1).round(1), A.mean(1).round(1))
