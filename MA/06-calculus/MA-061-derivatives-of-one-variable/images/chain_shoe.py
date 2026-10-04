"""The chain rule with two straight lines (Plotly frames): height = 2 x weight, shoe size = 1/4 x height.
Moving the weight moves the height twice as far, and the shoe size a quarter of that: 1/4 x 2 = 1/2.
Our own drawing of the numbers in StatQuest, "The Chain Rule, Clearly Explained!!!".
Run: python chain_shoe.py -> chain_shoe.gif, chain_shoe_frames.png"""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
A, B = 2.0, 0.25                         # d height / d weight, d shoe / d height
assert A * B == 0.5
W0 = 2.0


def frame(w):
    h, sh = A * w, B * A * w
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                        subplot_titles=("height = 2 × weight", "shoe size = ¼ × height"))
    fig.add_trace(go.Scatter(x=[0, 6], y=[0, 12], line=dict(color=GREEN, width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 12], y=[0, 3], line=dict(color=ORANGE, width=4)), row=1, col=2)
    for col, (x, y) in ((1, (w, h)), (2, (h, sh))):
        fig.add_trace(go.Scatter(x=[x, x, 0], y=[0, y, y], mode="lines", line=dict(color=GREY, width=2, dash="dot")),
                      row=1, col=col)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=18, color="black")), row=1, col=col)
    fig.update_xaxes(title="weight", range=[0, 6], dtick=1, row=1, col=1)
    fig.update_yaxes(title="height", range=[0, 12], dtick=2, row=1, col=1)
    fig.update_xaxes(title="height", range=[0, 12], dtick=2, row=1, col=2)
    fig.update_yaxes(title="shoe size", range=[0, 3], dtick=0.5, row=1, col=2)
    dw = w - W0
    change = "" if dw == 0 else (f"<br>weight +{dw:g}  →  height +{A * dw:g}  →  shoe size +{A * B * dw:g}"
                                 f"   (¼ × 2 = <b>½</b> per unit of weight)")
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=130, b=65),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"weight = {w:g}  →  height = {h:g}  →  shoe size = {sh:g}{change}"))
    fig.update_annotations(font_size=22)
    return fig


ws = [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.5, 5]
figs = [frame(w) for w in ws]
holds = [8 if w in (2, 3, 4) else 12 if w == 5 else 2 for w in ws]
make_gif(figs, here / "chain_shoe", fps=6, holds=holds, keys=[0, ws.index(3), ws.index(4), len(ws) - 1], width=1000)
