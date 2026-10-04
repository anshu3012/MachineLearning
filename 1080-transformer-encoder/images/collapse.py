"""Untrained encoder stacks on a real review: similarity between words, and of each word to its own input,
after each block, with and without residual connections (Plotly, mean of 5 random starts)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, GREY, FONT

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "collapse.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("similarity between the words", "similarity of each word to its own input"))
for res, name, col in ((True, "with residual connections", RED), (False, "without", GREY)):
    d = c[c.residual == res]
    for k, y in ((1, "between"), (2, "own")):
        fig.add_trace(go.Scatter(x=d.blocks, y=d[y], name=name, showlegend=(k == 1), mode="lines+markers",
                                 line=dict(color=col, width=4), marker=dict(size=6)), row=1, col=k)
for k in (1, 2):
    fig.add_vline(x=6, line=dict(color=GREY, dash="dot", width=1.5), row=1, col=k)
    fig.update_xaxes(title_text="number of encoder blocks", row=1, col=k)
    fig.update_yaxes(title_text="mean cosine similarity", range=[-0.1, 1.08], row=1, col=k)
fig.add_annotation(x=6, y=-0.05, text="6 blocks", showarrow=False, xanchor="left", xshift=4, row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=450, font=FONT, margin=dict(l=70, r=20, t=50, b=60),
                  legend=dict(x=0.25, y=0.55, bgcolor="rgba(255,255,255,0.85)"))
fig.update_annotations(font=FONT)
fig.write_image(here / "collapse.png", scale=2)
fig.write_image(here / "collapse.pdf")
