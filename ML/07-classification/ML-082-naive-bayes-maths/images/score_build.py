"""The MAP rule step by step (Plotly frames -> GIF), on the cricket example. Each frame multiplies both class scores
by one more factor: the prior, then P(toss lost | C), P(Mumbai | C), P(sunny | C). Win starts ahead (5/8 against
3/8) but its factor for a lost toss, 1/5, drops it behind; the final scores are 0.040 and 0.056, so the arg max is
loss."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED, make_gif
from nb_scores import FACTORS, NAMES, SCORE

here = Path(__file__).parent
run = {k: np.cumprod(v) for k, v in FACTORS.items()}
assert run["win"][0] > run["loss"][0] and run["win"][1] < run["loss"][1] and np.isclose(run["loss"][-1], SCORE["loss"])


def frame(i):
    fig = go.Figure()
    for k, c in (("win", BLUE), ("loss", RED)):
        fig.add_trace(go.Scatter(x=NAMES[:i + 1], y=run[k][:i + 1], mode="lines+markers+text", name=k,
                                 line=dict(color=c, width=4), marker=dict(size=14),
                                 text=[f"{v:.3f}" for v in run[k][:i + 1]], textposition="top center" if k == "loss" else "bottom center",
                                 textfont=dict(size=18, color=c)))
    lead = max(run, key=lambda k: run[k][i])
    fig.update_layout(template="simple_white", width=1050, height=560, font=FONT,
                      title=dict(text=f"after {i + 1} factor{'s' if i else ''}: {lead} leads" + (" → predict loss" if i == 3 else ""), x=0.5),
                      xaxis=dict(categoryorder="array", categoryarray=NAMES, range=[-0.4, 3.4]),
                      yaxis=dict(title="running score (log scale)", type="log", range=[-1.5, 0]),
                      legend=dict(x=0.8, y=0.98), margin=dict(l=80, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    make_gif([frame(i) for i in range(4)], here / "score_build", fps=1, holds=[2, 3, 2, 5], keys=[3], cols=1)
