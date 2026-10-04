"""The product rule as an area (Plotly), for the Note's dice events A: die 2 shows 6 and B: die 1 shows 3. The whole
square is the sample space (area 1). A is a band of width 1/6, B a band of height 1/6; because A takes the same 1/6
share inside B as outside it, the overlap is a 1/6 x 1/6 rectangle: P(A and B) = 1/36."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, PURPLE

here = Path(__file__).parent
pa = pb = 1 / 6
assert abs(pa * pb - 1 / 36) < 1e-15
fig = go.Figure()
fig.add_shape(type="rect", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=2), fillcolor="white", layer="below")
fig.add_shape(type="rect", x0=5 / 6, x1=1, y0=0, y1=1, fillcolor=BLUE, opacity=0.35, line_width=0)
fig.add_shape(type="rect", x0=0, x1=1, y0=2 / 6, y1=3 / 6, fillcolor=ORANGE, opacity=0.35, line_width=0)
fig.add_shape(type="rect", x0=5 / 6, x1=1, y0=2 / 6, y1=3 / 6, fillcolor=PURPLE, opacity=0.9, line=dict(color="black", width=2))
fig.add_annotation(x=11 / 12, y=0.85, text="A: die 2 = 6<br>width 1/6", showarrow=False, font=dict(size=20, color=BLUE))
fig.add_annotation(x=0.35, y=5 / 12, text="B: die 1 = 3, height 1/6", showarrow=False, font=dict(size=20, color=ORANGE))
fig.add_annotation(x=11 / 12, y=5 / 12, ax=-170, ay=110, text="A ∩ B: 1/6 × 1/6 = 1/36", font=dict(size=21, color=PURPLE),
                   arrowcolor=PURPLE, arrowwidth=2)
fig.update_layout(template="simple_white", width=700, height=700, font=FONT, showlegend=False,
                  xaxis=dict(visible=False, range=[-0.02, 1.02]), yaxis=dict(visible=False, range=[-0.02, 1.02], scaleanchor="x"),
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "product_area.png", scale=2)
