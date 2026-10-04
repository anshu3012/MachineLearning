"""Four test digits as they are (top) and with their pixels scrambled by one fixed permutation (bottom),
with the ANN's mean test accuracy on each version (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
d = np.load(here.parent / "data" / "scrambled_examples.npz")
acc = pd.read_csv(here.parent / "data" / "scramble_results.csv").groupby("images").test_acc.mean()
fig = make_subplots(2, 4, horizontal_spacing=0.02, vertical_spacing=0.08, row_titles=(
    f"normal: {100 * acc['normal']:.2f}%", f"scrambled: {100 * acc['scrambled']:.2f}%"))
for i in range(4):
    for r, key in ((1, "normal"), (2, "scrambled")):
        fig.add_trace(go.Heatmap(z=d[key][i], colorscale="gray", showscale=False), r, i + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False, autorange="reversed")
for i in range(1, 9):
    fig.layout[f"yaxis{'' if i == 1 else i}"].scaleanchor = f"x{'' if i == 1 else i}"
fig.update_layout(template="simple_white", width=1000, height=540, font=FONT, margin=dict(l=10, r=60, t=20, b=10))
fig.write_image(here / "scrambled.png", scale=2)
fig.write_image(here / "scrambled.pdf")
