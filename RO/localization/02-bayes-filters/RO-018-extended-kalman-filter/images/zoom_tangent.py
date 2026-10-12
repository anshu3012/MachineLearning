"""Zoom in on the beacon curve and it looks straight. Two windows shrink together, 8 m, 2 m, 0.5 m and 0.1 m wide, both
axes on the same scale: left, around x = 1 m, where the tangent line has slope -0.928; right, around x = 6 m under the
beacon, where the curve bends most and the tangent line is flat. Each panel prints the largest vertical gap between the
curve and its tangent line inside the window, as a share of the window's height.
Run: python zoom_tangent.py -> zoom_tangent.gif, zoom_tangent_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, PURPLE, make_gif
from ekfsim import dh, h

here = Path(__file__).parent
STOPS = [8.0, 2.0, 0.5, 0.1]                 # window widths (m) the zoom holds at
STEPS = 4                                    # in-between frames from one stop to the next
CENTRES = [1.0, 6.0]


def gap(c, w):
    """Largest vertical gap between h and its tangent line at c, inside the window c +- w/2 (m)."""
    g = np.linspace(c - w / 2, c + w / 2, 2001)
    return np.max(np.abs(h(g) - (h(c) + dh(c) * (g - c))))


def frame(w):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.15, subplot_titles=[
        f"at x = 1 m, slope {dh(1.0):.3f}".replace("-", "\u2212") + f"<br>largest gap: {100 * gap(1.0, w) / w:.2g}% of window height",
        f"at x = 6 m, under the beacon, slope 0<br>largest gap: {100 * gap(6.0, w) / w:.2g}% of window height"])
    for col, c in enumerate(CENTRES, start=1):
        g = np.linspace(c - w / 2, c + w / 2, 400)
        fig.add_trace(go.Scatter(x=g, y=h(g), line=dict(color="black", width=6, simplify=False)), row=1, col=col)
        fig.add_trace(go.Scatter(x=g, y=h(c) + dh(c) * (g - c), line=dict(color=PURPLE, width=3, dash="dash")),
                      row=1, col=col)
        fig.add_trace(go.Scatter(x=[c], y=[h(c)], mode="markers", marker=dict(color=PURPLE, size=13)), row=1, col=col)
        fig.update_xaxes(range=[c - w / 2, c + w / 2], nticks=5, title="position x (m)", row=1, col=col)
        fig.update_yaxes(range=[h(c) - w / 2, h(c) + w / 2], nticks=5, title="h(x) (m)", row=1, col=col)
    width = f"{w:.2g}".rstrip("0").rstrip(".") if w < 1 else f"{w:.1f}".rstrip("0").rstrip(".")
    fig.update_layout(template="simple_white", font=FONT, width=1050, height=645, showlegend=False,
                      margin=dict(l=90, r=30, t=170, b=80),
                      title=dict(x=0.5, y=0.955, yanchor="top", font=dict(size=25), text=(
                          f"window {width} m wide, both axes on the same scale<br>"
                          "<span style='font-size:19px'>black: beacon distance h(x)   "
                          "purple dashed: tangent line   purple dot: where it touches</span>")))
    fig.update_annotations(font=dict(size=20))
    return fig


widths, holds, keys = [], [], []
for i, w in enumerate(STOPS):
    if i:
        prev = STOPS[i - 1]
        widths += [prev * (w / prev) ** (k / STEPS) for k in range(1, STEPS)]
        holds += [1] * (STEPS - 1)
    keys.append(len(widths))
    widths.append(w)
    holds.append(10 if i == 0 else 24 if i == len(STOPS) - 1 else 8)
figs = [frame(w) for w in widths]
# square plot areas, so both axes really are on the same scale: (1050 - 90 - 30) * (1 - 0.15) / 2 = 645 - 170 - 80
assert abs((1050 - 90 - 30) * (1 - 0.15) / 2 - (645 - 170 - 80)) < 1
make_gif(figs, here / "zoom_tangent", fps=4, holds=holds, keys=keys, cols=2, width=900)

# numbers the Note quotes: h(1), the slope there and its chain-rule parts, and the gaps at the four stops
s = (6 - 1) ** 2 + 4
assert s == 29 and round(np.sqrt(s), 4) == 5.3852 == round(float(h(1.0)), 4)
assert round(1 / (2 * 5.3852), 4) == 0.0928 and round(0.0928 * -10, 3) == -0.928 == round(float(dh(1.0)), 3)
assert round(-5 / 5.3852, 3) == -0.928 and dh(6.0) == 0
pct = {w: (100 * gap(1.0, w) / w, 100 * gap(6.0, w) / w) for w in STOPS}
assert [f"{a:.2g}" for a, _ in pct.values()] == ["7.1", "0.77", "0.17", "0.032"], pct
assert [f"{b:.2g}" for _, b in pct.values()] == ["31", "12", "3.1", "0.62"], pct
