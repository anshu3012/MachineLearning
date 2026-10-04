"""One term of dL/dw_i per time step, for the one-node example on a 30-step sequence of ones: the bars are added
from the last time step backwards; each step back multiplies the term by about 0.26, so the far terms vanish.
Data: data/path_terms_by_length.csv (Notebook). Plotly frames: one more time step per frame.
Run: python long_paths.py -> long_paths.gif, long_paths_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import ORANGE, RED, GREY
from frames import save

HERE = Path(__file__).parent
t = pd.read_csv(HERE.parent / "data" / "path_terms_by_length.csv")
t = t[t["T"] == 30].sort_values("steps_back").reset_index(drop=True)
t["size"] = t.term.abs()
FONT = dict(family="Latin Modern Roman", size=22)
SHOW = 13                                                    # steps back drawn (the rest are below 1e-8)
assert t["size"].is_monotonic_decreasing and t["size"][10] < 1e-6


def frame(k):
    """Terms 0..k steps back."""
    d = t.iloc[:k + 1]
    fig = go.Figure(go.Bar(x=d.steps_back, y=d["size"], marker_color=[ORANGE] * k + [RED], width=0.7))
    fig.add_annotation(x=12.6, y=-0.3, xanchor="right", yanchor="top", showarrow=False, font=dict(size=22),
                       text=f"term {k} step{'s' if k != 1 else ''} back: {t['size'][k]:.2g}<br>"
                            f"sum of the {k + 1} term{'s' if k else ''} so far: {d['size'].sum():.4f}<br>"
                            f"<span style='color:{GREY}'>sum of all 30 terms: {t['size'].sum():.4f}</span>")
    fig.update_layout(template="simple_white", width=1000, height=580, font=FONT, showlegend=False,
                      title=dict(text="size of each time step's term in ∂L/∂w<sub>i</sub> (30-step sequence)", x=0.5),
                      xaxis=dict(title="time steps back from the output", range=[-0.6, SHOW - 0.4], dtick=1),
                      yaxis=dict(title="size of the term (log scale)", type="log", range=[-8, 0], dtick=1,
                                 exponentformat="power"),
                      margin=dict(l=100, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(SHOW)]
    seq = [0] * 3 + [k for k in range(SHOW) for _ in range(2)] + [SHOW - 1] * 8
    save("long_paths", figs, seq, [0, 2, 6, SHOW - 1], HERE, fps=3)
