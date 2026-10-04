"""What a log does to a number line: 1/8, 1/4, 1/2, 1, 2, 4, 8 slide from an ordinary axis to a log2 axis, where every
doubling or halving is one equal step and 8 times up is as far from 1 as 8 times down. Idea after StatQuest,
"Logs (logarithms), Clearly Explained!!!" (00:30-06:00). Plotly frames (points sliding on one line; no 3D or camera
motion that would need Manim) -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREEN

here = Path(__file__).parent
x = np.array([1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8])
NAMES = ["1/8", "1/4", "1/2", "1", "2", "4", "8"]
e = np.log2(x)
assert e.tolist() == [-3, -2, -1, 0, 1, 2, 3]
lin, log = x / 8, (e + 3) / 6  # both mapped to a 0-to-1 screen position


def frame(t, head, final=False):
    p = (1 - t) * lin + t * log
    fig = go.Figure()
    fig.add_shape(type="line", x0=0, x1=1, y0=0, y1=0, line=dict(color="black", width=2))
    top = t > 0.5  # early frames: the small values overlap, so label only 1, 2, 4, 8
    fig.add_scatter(x=p, y=[0] * 7, mode="markers+text", marker=dict(size=22, color=[RED] * 3 + ["black"] + [GREEN] * 3),
                    text=NAMES if top else [""] * 3 + NAMES[3:], textposition="top center", textfont=dict(size=24))
    if t == 0:
        fig.add_annotation(x=p[1], y=0.22, showarrow=False, text="1/8, 1/4, 1/2", font=dict(size=24, color=RED))
        fig.add_annotation(x=0.5, y=-0.5, showarrow=False, font=dict(size=22),
                           text="8 times up is far from 1; 8 times down is hardly visible")
    if final:
        fig.add_scatter(x=p, y=[-0.22] * 7, mode="text", text=[f"2<sup>{int(v)}</sup>" for v in e], textfont=dict(size=24))
        fig.add_scatter(x=p, y=[-0.5] * 7, mode="text", text=[f"log₂ = {int(v)}" for v in e], textfont=dict(size=20, color=BLUE))
        for a, b, col, lab in ((p[3], p[0], RED, "8 times down: 3 steps"), (p[3], p[6], GREEN, "8 times up: 3 steps")):
            fig.add_annotation(x=b, y=0.62, ax=a, ay=0.62, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                               arrowhead=2, arrowwidth=3, arrowcolor=col, text="")
            fig.add_annotation(x=(a + b) / 2, y=0.8, text=lab, showarrow=False, font=dict(size=22, color=col))
    fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, showlegend=False,
                      title=dict(text=f"<b>{head}</b>", x=0.5), margin=dict(l=40, r=40, t=80, b=20),
                      xaxis=dict(visible=False, range=[-0.06, 1.06]), yaxis=dict(visible=False, range=[-0.7, 1.0]))
    return fig


if __name__ == "__main__":
    ts = np.linspace(0, 1, 9)
    figs = [frame(0, "An ordinary number line")] + [frame(t, "Taking log₂ of every value …") for t in ts[1:-1]]
    figs += [frame(1, "The log₂ axis: the log keeps only the exponent", final=True)]
    save_gif(figs, "log_axis", here, keys=[0, 4, 8], fps=4, holds=[10] + [1] * 7 + [24], cols=1, width=860)
