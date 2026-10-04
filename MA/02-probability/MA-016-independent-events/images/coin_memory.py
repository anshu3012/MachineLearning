"""A coin has no memory (Plotly): one million sequences of four fair tosses (seed 0). For each number of heads in
the first three tosses, the share of sequences whose fourth toss is heads. Every bar is about 0.5: knowing the
first three tosses does not change the fourth, P(A | B) = P(A)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY

here = Path(__file__).parent
rng = np.random.default_rng(0)
T = rng.integers(0, 2, size=(1_000_000, 4))
first = T[:, :3].sum(1)
share = [T[first == k, 3].mean() for k in range(4)]
counts = [int((first == k).sum()) for k in range(4)]
assert all(abs(s - 0.5) < 0.005 for s in share) and round(share[3], 3) == 0.499
labels = ["0 heads", "1 head", "2 heads", "3 heads"]
fig = go.Figure(go.Bar(x=labels, y=share, marker_color=BLUE, text=[f"{s:.3f}<br>({c:,} sequences)" for s, c in zip(share, counts)],
                       textposition="outside", textfont=dict(size=17)))
fig.add_hline(y=0.5, line=dict(color=GREY, dash="dash", width=2), opacity=1)
fig.update_layout(template="simple_white", width=950, height=520, font=FONT,
                  xaxis=dict(title="heads in the first three tosses"), yaxis=dict(title="share with heads on toss 4", range=[0, 0.7]),
                  margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "coin_memory.png", scale=2)
