"""Section 5: why one sine wave is not enough. Left: sin(pos) for positions 1 to 1,000; positions 11 and 344 land at
almost the same height. Right: the pair (sin pos, cos pos) puts every position on a circle; positions 15 and 725 land
almost on the same point. Pairs from data/closest_pairs.csv (Notebook). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
C = pd.read_csv(here.parent / "data" / "closest_pairs.csv")
a1, b1 = C.loc[0, ["pos_a", "pos_b"]].astype(int)
a2, b2 = C.loc[1, ["pos_a", "pos_b"]].astype(int)
assert (a1, b1, a2, b2) == (11, 344, 15, 725) and abs(np.sin(a1) - np.sin(b1)) < 2e-7
pos = np.arange(1, 1001)
fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.1,
                    subplot_titles=("one number: sin(pos)", "two numbers: (sin pos, cos pos)"))
fig.add_scatter(x=pos, y=np.sin(pos), mode="markers", marker=dict(size=3, color=GREY), showlegend=False, row=1, col=1)
fig.add_scatter(x=[a1, b1], y=np.sin([a1, b1]), mode="markers+text", text=[f"pos {a1}", f"pos {b1}"],
                textposition="top center", marker=dict(size=13, color=RED), showlegend=False, textfont=dict(color=RED), row=1, col=1)
fig.add_hline(y=np.sin(a1), line=dict(color=RED, dash="dot", width=1.5), row=1, col=1)
fig.update_xaxes(title="position", row=1, col=1)
fig.update_yaxes(range=[-1.25, 1.35], row=1, col=1)
fig.add_scatter(x=np.sin(pos), y=np.cos(pos), mode="markers", marker=dict(size=3, color=GREY), showlegend=False, row=1, col=2)
fig.add_scatter(x=np.sin([a2, b2]), y=np.cos([a2, b2]), mode="markers+text", text=[f"pos {a2}", f"pos {b2}"],
                textposition=["top left", "bottom right"], marker=dict(size=13, color=BLUE, symbol=["circle", "x"]),
                showlegend=False, textfont=dict(color=BLUE), row=1, col=2)
fig.update_xaxes(title="sin(pos)", range=[-1.3, 1.3], row=1, col=2)
fig.update_yaxes(title="cos(pos)", range=[-1.3, 1.3], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, font=dict(FONT, size=18), margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "sine_collisions.png", scale=2)
fig.write_image(here / "sine_collisions.pdf")
