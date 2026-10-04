"""Sliding the threshold along the rating feature (Plotly frames -> GIF). Left: the 8 observations on the rating axis
(green = downloaded, red = not) with the candidate threshold. Right: the information gain of every threshold tried so
far. The peak, 0.549 at rating <= 3.2, becomes the question at this node."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
rating = np.array([1.6, 2.1, 2.9, 3.2, 3.3, 3.5, 4.1, 4.6])
down = np.array([0, 0, 0, 0, 1, 0, 1, 1])


def H(v):
    p = np.bincount(v, minlength=2) / len(v)
    p = p[p > 0]
    return abs(float(-(p * np.log2(p)).sum()))


def split(v):
    L, R = down[rating <= v], down[rating > v]
    return H(L), H(R), H(down) - (len(L) * H(L) + len(R) * H(R)) / 8


G = [split(v)[2] for v in rating[:-1]]
best = int(np.argmax(G))
assert round(H(down), 3) == 0.954 and rating[best] == 3.2 and round(G[best], 3) == 0.549


def frame(k, final=False):
    v = rating[k]
    hl, hr, g = split(v)
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.13,
                        subplot_titles=[f"split: rating ≤ {v}", "information gain so far"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=rating, y=[0] * 8, mode="markers", marker=dict(size=22, color=[GREEN if d else RED for d in down],
                             line=dict(color="black", width=1))), 1, 1)
    cut = (v + rating[k + 1]) / 2
    fig.add_shape(type="line", x0=cut, x1=cut, y0=-0.6, y1=0.6, line=dict(color=BLUE, width=4), opacity=1, row=1, col=1)
    fig.add_annotation(x=2.2, y=0.85, text=f"left: H = {hl:.3f}", showarrow=False, font=dict(size=20), row=1, col=1)
    fig.add_annotation(x=4.1, y=-0.85, text=f"right: H = {hr:.3f}", showarrow=False, font=dict(size=20), row=1, col=1)
    fig.update_xaxes(range=[1.2, 5.0], title="rating (green = downloaded, red = not)", row=1, col=1)
    fig.update_yaxes(range=[-1.1, 1.1], visible=False, row=1, col=1)
    xs = [f"≤ {r}" for r in rating[:-1]]
    done = k + 1
    cols = [GREEN if (final and i == best) else (BLUE if i == k and not final else GREY) for i in range(done)]
    fig.add_trace(go.Bar(x=xs[:done], y=G[:done], marker_color=cols, text=[f"{x:.2f}" for x in G[:done]], textposition="outside",
                         textfont=dict(size=17)), 1, 2)
    fig.update_xaxes(categoryorder="array", categoryarray=xs, range=[-0.5, 6.5], tickfont=dict(size=17), row=1, col=2)
    fig.update_yaxes(range=[0, 0.68], title="information gain", row=1, col=2)
    title = "the peak, rating ≤ 3.2 (gain 0.549), becomes the question" if final else f"gain = {g:.3f}"
    fig.update_layout(template="simple_white", width=1200, height=540, font=FONT, showlegend=False,
                      margin=dict(l=40, r=30, t=120, b=80), title=dict(text=title, x=0.5, y=0.96, font=dict(size=24)))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(7)]
    final = frame(3, final=True)
    final.data[1].update(x=[f"≤ {r}" for r in rating[:-1]], y=G, text=[f"{x:.2f}" for x in G],
                         marker_color=[GREEN if i == best else GREY for i in range(7)])
    figs.append(final)
    make_gif(figs, here / "threshold_sweep", fps=1, holds=[2] * 7 + [5], keys=[1, 7], cols=1)
