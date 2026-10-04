"""Gradient descent on the non-convex curve of the loss-shapes figure, L(w) = 0.15 w^4 - 0.9 w^2 + 0.35 w + 2.2, from
two starting points (w = -2.7 and w = 2.7), learning rate 0.07. Each run only follows its local slope: the left
start reaches the global minimum, the right start stops in the local minimum. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import make_gif, FONT, BLUE, ORANGE, GREEN, GREY

here = Path(__file__).parent
f = lambda w: 0.15 * w ** 4 - 0.9 * w ** 2 + 0.35 * w + 2.2
df = lambda w: 0.6 * w ** 3 - 1.8 * w + 0.35
LR, N = 0.07, 30
paths = []
for w in (-2.7, 2.7):
    p = [w]
    for _ in range(N):
        p.append(p[-1] - LR * df(p[-1]))
    paths.append(np.array(p))
grid = np.linspace(-3, 3, 400)
w_glob, w_loc = paths[0][-1], paths[1][-1]
assert w_glob < 0 < w_loc and f(w_glob) < f(w_loc) and abs(df(w_glob)) < 0.01 and abs(df(w_loc)) < 0.01
print("ends", round(w_glob, 2), round(f(w_glob), 2), "|", round(w_loc, 2), round(f(w_loc), 2))


def frame(k, last=False):
    fig = go.Figure()
    fig.add_scatter(x=grid, y=f(grid), mode="lines", line=dict(color=BLUE, width=4))
    for p, col, name in ((paths[0], GREEN, "start A"), (paths[1], ORANGE, "start B")):
        fig.add_scatter(x=p[:k + 1], y=f(p[:k + 1]), mode="lines+markers", line=dict(color=col, width=1.5),
                        marker=dict(size=7, color=col), opacity=0.5)
        fig.add_scatter(x=[p[k]], y=[f(p[k])], mode="markers", marker=dict(size=22, color=col, line=dict(color="white", width=2)))
        fig.add_annotation(x=p[0], y=f(p[0]), text=name, ax=0, ay=-40, font=dict(size=22, color=col), arrowcolor=col)
    if last:
        fig.add_annotation(x=w_glob, y=f(w_glob), ax=0, ay=60, text=f"<b>global minimum</b><br>loss {f(w_glob):.2f}",
                           font=dict(size=21, color=GREEN), arrowcolor=GREEN)
        fig.add_annotation(x=w_loc, y=f(w_loc), ax=0, ay=60, text=f"<b>local minimum</b><br>loss {f(w_loc):.2f}: stuck here",
                           font=dict(size=21, color=ORANGE), arrowcolor=ORANGE)
    head = ("Same rule, two starting points" if k == 0 else
            "Where gradient descent ends depends on where it starts" if last else f"step {k}: each ball follows its own slope downhill")
    fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, font=dict(size=25)), margin=dict(l=80, r=30, t=80, b=70),
                      xaxis=dict(title="parameter w", range=[-3.2, 3.2]), yaxis=dict(title="loss", range=[-1.1, 5.4]))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(N + 1)] + [frame(N, last=True)]
    make_gif(figs, here / "two_starts", fps=5, holds=[6] + [1] * N + [18], keys=[0, N + 1], cols=2, width=800)
