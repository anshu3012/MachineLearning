"""Where the parameters are (layer norms, 2,048 and 3,072, are too small to see and are left out of the bars): one encoder block vs one decoder block, by part (Plotly, stacked bars).
Numbers are the formulas checked against Keras in the Notebook (d = 512, d_ff = 2048)."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, ORANGE, RED, FONT

here = Path(__file__).parent
d, d_ff = 512, 2048
mha, ffn = 4 * d * d + 4 * d, 2 * d * d_ff + d_ff + d
parts = [("masked self-attention", RED, [0, mha]), ("self-attention", ORANGE, [mha, 0]),
         ("cross-attention", "#9D755D", [0, mha]), ("feed-forward network", BLUE, [ffn, ffn])]
blocks = ["encoder block", "decoder block"]
fig = go.Figure()
for name, c, vals in parts:
    fig.add_trace(go.Bar(y=blocks, x=[v / 1e6 for v in vals], name=name, orientation="h", marker_color=c,
                         text=[f"{v / 1e6:.2f}M" if v > 1e5 else "" for v in vals], textposition="inside",
                         insidetextfont=dict(color="white")))
totals = [mha + ffn + 4 * d, 2 * mha + ffn + 6 * d]
for b, t in zip(blocks, totals):
    fig.add_annotation(y=b, x=t / 1e6, text=f"  {t:,}", showarrow=False, xanchor="left", font=FONT)
fig.update_layout(template="simple_white", barmode="stack", width=950, height=330, font=FONT,
                  xaxis=dict(title="parameters (millions)", range=[0, 5.3]),
                  legend=dict(orientation="h", y=1.25, x=0, traceorder="normal"), margin=dict(l=120, r=30, t=60, b=60))
fig.write_image(here / "param_parts.png", scale=2)
fig.write_image(here / "param_parts.pdf")
