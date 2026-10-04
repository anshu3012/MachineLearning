"""Entropy as average surprise (Plotly frames -> GIF). Three sets from the Note: 1 yes / 4 no, 2 yes / 3 no and
5 yes / 5 no. Left: the share p of each class. Right: the surprise log2(1/p) of each class, then the entropy as the
share-weighted average of the two surprises (dashed line): 0.722, 0.971 and 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, RED, make_gif

here = Path(__file__).parent
SETS = [(1, 4), (2, 3), (5, 5)]


def frame(k, show_h):
    a, b = SETS[k]
    p = np.array([a, b]) / (a + b)
    s = np.log2(1 / p)
    h = float((p * s).sum())
    fig = make_subplots(1, 2, horizontal_spacing=0.14, subplot_titles=["share p of each class", "surprise = log₂(1/p)"])
    fig.update_annotations(font_size=22)
    names = [f"yes ({a})", f"no ({b})"]
    fig.add_trace(go.Bar(x=names, y=p, marker_color=[GREEN, RED], text=[f"{v:.1f}" for v in p], textposition="outside",
                         textfont=dict(size=20)), 1, 1)
    fig.add_trace(go.Bar(x=names, y=s, marker_color=[GREEN, RED], text=[f"{v:.2f}" for v in s], textposition="outside",
                         textfont=dict(size=20)), 1, 2)
    title = f"{a} yes, {b} no: the rarer class is the bigger surprise" if a != b else f"{a} yes, {b} no: both classes surprise equally"
    if show_h:
        fig.add_shape(type="line", x0=-0.5, x1=1.5, y0=h, y1=h, line=dict(color=BLUE, width=4, dash="dash"), opacity=1, layer="above", row=1, col=2)
        title = f"entropy = {p[0]:.1f} × {s[0]:.2f} + {p[1]:.1f} × {s[1]:.2f} = {h:.3f}  (average surprise)"
    fig.update_yaxes(range=[0, 1.15], title="share", row=1, col=1)
    fig.update_yaxes(range=[0, 2.7], title="surprise (bits)", row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                      margin=dict(l=70, r=30, t=120, b=60), title=dict(text=title, x=0.5, y=0.96, font=dict(size=24)))
    return fig, h


if __name__ == "__main__":
    figs, hs = [], []
    for k in range(3):
        for show in (False, True):
            f, h = frame(k, show)
            figs.append(f)
        hs.append(round(h, 3))
    assert hs == [0.722, 0.971, 1.0], hs
    make_gif(figs, here / "surprise", fps=1, holds=[3, 4] * 3, keys=[1, 5], cols=1)
