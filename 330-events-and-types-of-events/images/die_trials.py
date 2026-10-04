"""The five terms in motion: the random experiment "roll a die" run in 12 trials. Each trial gives one outcome from
the sample space {1, ..., 6}; the event A = "an odd number" = {1, 3, 5} happens when the outcome lies in A.
Simulated rolls (seed 4). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, BLUE, ORANGE, GREEN

here = Path(__file__).parent
rolls = np.random.default_rng(4).integers(1, 7, 12)
A = {1, 3, 5}


def frame(k):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.08,
                        subplot_titles=["sample space S; event A = {1, 3, 5} in orange", "trials so far"])
    out = rolls[k - 1] if k else None
    for f in range(1, 7):
        c = ORANGE if f in A else "#e6e6e6"
        fig.add_shape(type="rect", x0=f - 0.45, x1=f + 0.45, y0=0, y1=1, fillcolor=c, opacity=1,
                      line=dict(color="black" if f == out else "white", width=6), row=1, col=1)
        fig.add_annotation(x=f, y=0.5, text=f"<b>{f}</b>", showarrow=False, font=dict(size=30), row=1, col=1)
    xs = np.arange(1, k + 1)
    hit = np.array([r in A for r in rolls[:k]])
    fig.add_scatter(x=xs, y=rolls[:k], mode="markers+text", text=[str(r) for r in rolls[:k]], textposition="top center",
                    marker=dict(size=20, color=np.where(hit, ORANGE, "#9a9a9a")), textfont=dict(size=18), row=1, col=2)
    fig.update_xaxes(visible=False, range=[0.4, 6.6], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-0.3, 1.3], row=1, col=1)
    fig.update_xaxes(title_text="trial", range=[0.3, 12.7], dtick=1, row=1, col=2)
    fig.update_yaxes(title_text="outcome", range=[0.3, 7], dtick=1, row=1, col=2)
    if k == 0:
        head = "Random experiment: roll a die"
    else:
        head = (f"Trial {k}: outcome <b>{out}</b> → event A {'happens' if out in A else 'does not happen'}"
                f"   (A so far: {hit.sum()} of {k})")
    fig.update_annotations(selector=dict(xref="paper"), font_size=20)
    fig.update_layout(template="simple_white", width=1300, height=480, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=60, r=30, t=100, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(13)], "die_trials", here, keys=[1, 12], fps=1, holds=[3] + [2] * 11 + [6], cols=1,
             width=900)
