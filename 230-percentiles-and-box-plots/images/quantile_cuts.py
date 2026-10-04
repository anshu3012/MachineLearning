"""Quantiles as cuts. The 244 total bills of the tips data as dots on a line. One cut (the median) makes 2 equal
groups; cutting each half again makes 4 equal groups of 61 (the quartiles); the box of a box plot spans the two middle
groups. Plotly frames -> GIF. Idea after StatQuest, "Quantiles and Percentiles, Clearly Explained!!!"."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREEN, PURPLE, GREY

here = Path(__file__).parent
bill = np.sort(pd.read_csv(here.parent / "data" / "tips.csv").total_bill.to_numpy())
q1, q2, q3 = np.percentile(bill, [25, 50, 75], method="weibull")       # the (n+1) rule of section 3.1
jit = np.random.default_rng(0).uniform(-1, 1, len(bill))
assert len(bill) == 244 and [(bill < q).sum() for q in (q1, q2, q3)] == [61, 122, 183]
print("Q1, Q2, Q3:", q1, q2, q3)


def frame(cuts, title, box=False):
    fig = go.Figure()
    edges = [0] + [c for c, _ in cuts] + [60]
    cols = {1: [GREY], 2: [BLUE, ORANGE], 4: [BLUE, GREEN, ORANGE, PURPLE]}[len(edges) - 1]
    if box:
        fig.add_shape(type="rect", x0=q1, x1=q3, y0=-1.5, y1=1.5, line=dict(color="black", width=3),
                      fillcolor="rgba(0,0,0,0.07)")
        fig.add_annotation(x=(q1 + q3) / 2, y=-2.1, text="<b>the box: middle half, 122 bills</b>", showarrow=False,
                           font=dict(size=22))
    for lo, hi, c in zip(edges[:-1], edges[1:], cols):
        m = (bill >= lo) & (bill < hi)
        fig.add_scatter(x=bill[m], y=jit[m], mode="markers", marker=dict(size=9, color=c, opacity=0.8,
                        line=dict(color="white", width=0.5)))
        if len(cols) > 1:
            fig.add_annotation(x=bill[m].mean() if hi < 60 else 34, y=2.1, text=f"<b>{m.sum()}</b>", showarrow=False,
                               font=dict(size=26, color=c))
    for c, name in cuts:
        fig.add_shape(type="line", x0=c, x1=c, y0=-1.7, y1=1.7, line=dict(color="black", width=3), opacity=1)
        fig.add_annotation(x=c, y=-1.9 if not box else -2.6, text=f"<b>{name}</b><br>{c:.1f}", showarrow=False,
                           font=dict(size=24), yanchor="top")
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5), margin=dict(l=30, r=30, t=80, b=80),
                      xaxis=dict(title="total bill (dollars), sorted from smallest to largest", range=[0, 53]),
                      yaxis=dict(visible=False, range=[-4.2, 2.8]))
    return fig


if __name__ == "__main__":
    three = [(q1, "Q1"), (q2, "Q2"), (q3, "Q3")]
    figs = [frame([], "<b>244 bills</b>, one dot each"),
            frame([(q2, "median")], "<b>One cut in the middle</b>: 2 equal groups"),
            frame(three, "<b>Cut each half again</b>: 4 equal groups. The cuts are the quartiles"),
            frame(three, "<b>Q1 to Q3</b> becomes the box of the box plot", box=True)]
    save_gif(figs, "quantile_cuts", here, keys=[0, 1, 2, 3], fps=1, holds=[2, 3, 4, 5])
