"""Section 3.1: memory of one 224 x 224 x 3 image, of its 222 x 222 x 100 feature maps, of a batch of 100 such
outputs, and of one image's maps after 2 x 2 max pooling (section 7.1); 4-byte floats (Plotly)."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
B = 4
rows = [("input image<br>224 × 224 × 3", 224 * 224 * 3 * B, GREY),
        ("feature maps, 1 image<br>222 × 222 × 100", 222 * 222 * 100 * B, BLUE),
        ("feature maps,<br>batch of 100", 100 * 222 * 222 * 100 * B, RED),
        ("after 2 × 2 max pool,<br>111 × 111 × 100", 111 * 111 * 100 * B, GREEN)]
assert round(rows[1][1] / 1e6, 1) == 19.7 and round(rows[2][1] / 1e9, 2) == 1.97 and round(rows[3][1] / 1e6, 1) == 4.9
lab = lambda b: f"{b / 1e9:.2f} GB" if b >= 1e9 else f"{b / 1e6:.1f} MB"
fig = go.Figure(go.Bar(x=[r[0] for r in rows], y=[r[1] / 1e6 for r in rows], marker_color=[r[2] for r in rows],
                       text=[lab(r[1]) for r in rows], textposition="outside", textfont=dict(size=20)))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(FONT, size=17),
                  yaxis=dict(type="log", title="memory (MB, log scale)", range=[-0.6, 3.9], tickvals=[1, 10, 100, 1000]),
                  margin=dict(l=80, r=20, t=20, b=90), xaxis=dict(tickangle=0))
fig.write_image(here / "memory_bars.png", scale=2)
fig.write_image(here / "memory_bars.pdf")
