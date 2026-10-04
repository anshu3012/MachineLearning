"""Two sequences of different lengths against an ANN's fixed input. Real weekly share prices (Google and Netflix,
January-February 2018, each divided by its price on 1 January 2018; from plotly.express.data.stocks(), stored in
data/stock_weeks.csv): 9 weeks of history for one share, 5 for the other. An input layer built for 9 numbers is
filled by the first and left with 4 empty inputs by the second. Plotly frames -> GIF, plus a key-frame grid.
Tool: Plotly frames, because a data series grows over time."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, RED, GREY, FONT
from gifkit import save_gif

HERE = Path(__file__).parent
D = pd.read_csv(HERE.parent / "data" / "stock_weeks.csv")
A, B = D.GOOG.tolist(), D.NFLX.tolist()[:5]          # 9 weeks of one share, 5 of the other
SLOTS = 9
assert len(A) == 9 and len(B) == 5


def boxes(fig, y, vals, n_shown, colour, label):
    """One row of 9 input slots; the first n_shown hold the series' values."""
    for k in range(SLOTS):
        filled = k < n_shown and k < len(vals)
        missing = n_shown >= len(vals) and k >= len(vals)
        fig.add_shape(type="rect", x0=k + 0.05, x1=k + 0.95, y0=y, y1=y + 0.8, row=2, col=1,
                      line=dict(color=RED if missing else "black", width=2, dash="dash" if missing else "solid"),
                      fillcolor=colour if filled else "white", opacity=0.9)
        txt = f"{vals[k]:.2f}" if filled else ("?" if missing else "")
        fig.add_annotation(x=k + 0.5, y=y + 0.4, text=txt, showarrow=False, row=2, col=1,
                           font=dict(size=18, color="white" if filled else RED))
    fig.add_annotation(x=-0.15, y=y + 0.4, text=label, showarrow=False, xanchor="right", row=2, col=1, font=dict(size=18, color=colour))


def frame(na, nb):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.2)
    wk = list(range(1, 10))
    fig.add_scatter(x=wk[:na], y=A[:na], mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=10),
                    name="share A: 9 weeks", row=1, col=1)
    if nb:
        fig.add_scatter(x=wk[:nb], y=B[:nb], mode="lines+markers", line=dict(color=ORANGE, width=4), marker=dict(size=10),
                        name="share B: 5 weeks", row=1, col=1)
    boxes(fig, 1.1, A, na, BLUE, "share A")
    boxes(fig, 0.0, B, nb, ORANGE, "share B")
    if nb >= len(B):
        title = "share B fills only 5 of the 9 inputs: <b>4 inputs have no value</b>"
    elif nb:
        title = f"share B: week {nb} of 5"
    elif na >= 9:
        title = "share A fills all <b>9 inputs</b> of the ANN"
    else:
        title = f"share A: week {na} of 9"
    fig.update_xaxes(title="week", range=[0.5, 9.5], dtick=1, row=1, col=1)
    fig.update_yaxes(title="price (week 1 = 1)", range=[0.9, 1.5], row=1, col=1)
    fig.update_xaxes(visible=False, range=[-2.2, 9.2], row=2, col=1)
    fig.update_yaxes(visible=False, range=[-0.2, 2.5], row=2, col=1)
    fig.add_annotation(x=4.5, y=2.25, text="the ANN's input layer: 9 inputs, fixed when the network is built",
                       showarrow=False, row=2, col=1, font=dict(size=18, color=GREY))
    fig.update_layout(template="simple_white", width=1000, height=700, font=dict(FONT, size=20),
                      title=dict(text=title, x=0.5, y=0.96), showlegend=True,
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=80, r=20, t=70, b=20))
    return fig


if __name__ == "__main__":
    steps = [(a, 0) for a in (1, 3, 5, 7, 9)] + [(9, b) for b in (1, 3, 5)]
    save_gif([frame(a, b) for a, b in steps], "series_lengths", HERE, keys=[4, 7], fps=1.2, cols=2,
             holds=[1, 1, 1, 1, 3, 1, 1, 5])
