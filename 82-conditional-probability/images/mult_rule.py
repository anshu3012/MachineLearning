"""The multiplication rule as an area (Plotly), on the breakfast-and-lunch numbers: P(A) = 0.6 (bagel for breakfast),
P(B) = 0.5 (pizza for lunch), P(A | B) = 0.7. Left: split the unit square by B (width 0.5), then shade A's share of the
B strip (height 0.7): area 0.35. Right: split by A (width 0.6), then shade B's share of the A strip (height 0.35/0.6 =
0.58): the same area 0.35."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, RED

here = Path(__file__).parent
pA, pB, pAgB = 0.6, 0.5, 0.7
both = pAgB * pB
pBgA = both / pA
assert round(both, 2) == 0.35 and round(pBgA, 2) == 0.58
fig = make_subplots(1, 2, horizontal_spacing=0.14, subplot_titles=["P(A | B) × P(B) = 0.7 × 0.5 = 0.35", "P(B | A) × P(A) = 0.58 × 0.6 = 0.35"])
fig.update_annotations(font_size=22)
for col, (w, h, first, second) in enumerate([(pB, pAgB, "B: pizza", "A given B"), (pA, pBgA, "A: bagel", "B given A")], 1):
    kw = dict(row=1, col=col)
    fig.add_shape(type="rect", x0=0, x1=1, y0=0, y1=1, fillcolor="white", line=dict(color="black", width=2), **kw)
    fig.add_shape(type="rect", x0=0, x1=w, y0=0, y1=1, fillcolor="#C9D7E8", line=dict(color=BLUE, width=2), **kw)
    fig.add_shape(type="rect", x0=0, x1=w, y0=0, y1=h, fillcolor=RED, opacity=0.75, line=dict(color=RED, width=2), **kw)
    fig.add_annotation(x=w / 2, y=h / 2, text="both<br>0.35", showarrow=False, font=dict(size=24, color="white"), **kw)
    fig.add_annotation(x=w / 2, y=1.06, text=f"{first}, width {w}", showarrow=False, font=dict(size=20, color=BLUE), **kw)
    fig.add_annotation(x=w + 0.02, y=h / 2, text=f"{second}:<br>height {h:.2f}".replace("0.70", "0.7"), showarrow=False, xanchor="left", font=dict(size=20, color=RED), **kw)
    fig.update_xaxes(range=[-0.02, 1.02], dtick=0.5, **kw)
    fig.update_yaxes(range=[-0.02, 1.12], dtick=0.5, scaleanchor=f"x{col if col > 1 else ''}", **kw)
fig.update_layout(template="simple_white", width=1200, height=620, font=FONT, margin=dict(l=50, r=20, t=70, b=40))
fig.write_image(here / "mult_rule.png", scale=2)
