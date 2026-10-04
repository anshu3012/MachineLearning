"""Section 7.3: translation quality and size against the number of encoder (and decoder) blocks N, from Vaswani et al.
(2017), Table 3, rows C (English-to-German, development set). Numbers typed from the paper, as in the Note's table.
Run: python bleu_blocks.py  -> bleu_blocks.png (Plotly: BLEU line with parameter labels)"""
from pathlib import Path

import plotly.graph_objects as go

from common import RED

HERE = Path(__file__).parent
N, bleu, params = [2, 4, 6, 8], [23.7, 25.3, 25.8, 25.5], [36, 50, 65, 80]
assert round(bleu[2] - bleu[0], 1) == 2.1                      # the Note: 2 -> 6 blocks adds 2.1 BLEU

fig = go.Figure(go.Scatter(x=N, y=bleu, mode="lines+markers+text", line=dict(color=RED, width=4),
                           marker=dict(size=[14, 14, 22, 14]), text=[f"{b}<br>({m} M parameters)" for b, m in zip(bleu, params)],
                           textposition=["bottom right", "top left", "top center", "bottom center"]))
fig.update_layout(template="simple_white", width=1000, height=480, font=dict(family="Latin Modern Roman", size=22),
                  xaxis=dict(title="blocks N", tickvals=N, range=[1.5, 9.3]), yaxis=dict(title="BLEU", range=[23.2, 26.5]),
                  margin=dict(l=80, r=30, t=30, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "bleu_blocks.png", scale=2)
