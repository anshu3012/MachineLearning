"""A one-unit LSTM reading two sales series that differ only on day 1: the input, the cell state (long-term memory)
and the hidden state (short-term memory), day by day. The last hidden state is the prediction for day 5.
Data: data/two_series_states.csv (Notebook, first seed). Plotly frames: one day per frame.
Run: python two_series.py -> two_series.gif, two_series_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY
from frames import save

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "two_series_states.csv")
FONT = dict(family="Latin Modern Roman", size=22)
SHOPS = (("A", ORANGE, 0.0), ("B", BLUE, 1.0))
COLS = (("sales", "input: sales that day", [-0.1, 1.15]), ("cell_state", "long-term memory (cell state)", [-1, 3.9]),
        ("hidden_state", "short-term memory (hidden state)", [-0.6, 1.25]))
last = d[d.day == 4].set_index("shop").hidden_state
assert abs(last["A"]) < 0.05 and last["B"] > 0.95                      # day 1 is remembered on day 4


def frame(day, final=False):
    fig = make_subplots(1, 3, horizontal_spacing=0.07, subplot_titles=[c[1] for c in COLS])
    for k, (col, _, rng) in enumerate(COLS, start=1):
        for shop, colour, target in SHOPS:
            s = d[(d.shop == shop) & (d.day <= day)]
            fig.add_trace(go.Scatter(x=s.day, y=s[col], mode="lines+markers+text", line=dict(color=colour, width=4),
                                     marker=dict(size=12), text=[""] * (len(s) - 1) + ["" if final and col == "hidden_state" else f"{shop}: {s[col].iloc[-1] + 0.0:.2f}".replace("-0.00", "0.00")],
                                     textposition="top center" if shop == "B" else "bottom center",
                                     textfont=dict(color=colour, size=20)), 1, k)
            if final and col == "hidden_state":
                fig.add_trace(go.Scatter(x=[5], y=[target], mode="markers+text", text=[f"true day 5: {target:g}"],
                                         textposition="top center" if shop == "B" else "bottom center", textfont=dict(color=colour, size=20),
                                         marker=dict(size=16, color="white", line=dict(color=colour, width=3))), 1, k)
        fig.update_yaxes(range=rng, row=1, col=k)
        fig.update_xaxes(range=[0.5, 5.9], tickvals=[1, 2, 3, 4, 5], title="day", row=1, col=k)
    fig.update_annotations(font=dict(size=22))
    title = (f"day {day}: " + ("the two shops differ" if day == 1 else "same sales in both shops, but the memories stay apart")
             if not final else "the last hidden state predicts day 5: A 0.00 (true 0), B 0.99 (true 1)")
    fig.update_layout(template="simple_white", width=1300, height=500, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=50, r=20, t=110, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in (1, 2, 3, 4)] + [frame(4, final=True)]
    save("two_series", figs, [0] * 3 + [1] * 2 + [2] * 2 + [3] * 2 + [4] * 6, [0, 1, 3, 4], HERE, fps=1.2, gif_width=900)
