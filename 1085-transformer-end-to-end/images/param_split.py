"""Section 4.3: where the base model's 63,082,496 parameters sit (Notebook's Keras model, shared 37,000-token
embedding). Counts as in the Note's table.
Run: python param_split.py  -> param_split.png (Plotly stacked bar)"""
from pathlib import Path

import plotly.graph_objects as go

from common import BLUE, GREY, ORANGE

HERE = Path(__file__).parent
enc, dec, emb = 6 * 3152384, 6 * 4204032, 37000 * 512
assert enc + dec == 44138496 and emb == 18944000 and enc + dec + emb == 63082496
fig = go.Figure()
for name, v, c in (("6 encoder blocks", enc, BLUE), ("6 decoder blocks", dec, ORANGE), ("shared embedding", emb, GREY)):
    fig.add_trace(go.Bar(y=["base model"], x=[v / 1e6], orientation="h", name=f"{name}: {v:,}", marker_color=c,
                         text=f"{v / 1e6:.1f} M", textposition="inside", textfont=dict(size=24, color="white")))
fig.update_layout(template="simple_white", barmode="stack", width=1100, height=360,
                  font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="63,082,496 parameters (paper: 65 million)", x=0.5, y=0.95),
                  xaxis=dict(title="parameters (millions)", range=[0, 66]), yaxis=dict(visible=False),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.75, yanchor="top", traceorder="normal"),
                  margin=dict(l=20, r=30, t=60, b=150))

if __name__ == "__main__":
    fig.write_image(HERE / "param_split.png", scale=2)
