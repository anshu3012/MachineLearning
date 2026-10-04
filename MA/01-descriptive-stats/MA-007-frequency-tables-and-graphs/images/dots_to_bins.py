"""Why a histogram exists. The 244 total bills of the tips data as dots on one line: they hide each other. Stacking
equal values barely helps (few bills repeat). Cutting the line into bins 5 wide and stacking the dots in each bin
gives the histogram. Plotly frames -> GIF. Idea after StatQuest, "Histograms, Clearly Explained"."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREY

here = Path(__file__).parent
bill = np.sort(pd.read_csv(here.parent / "data" / "tips.csv").total_bill.to_numpy())
N, W, PER_ROW, YMAX = len(bill), 5, 4, 76
edges = np.arange(0, 56, W)
counts, _ = np.histogram(bill, edges)
assert N == 244 and counts.sum() == N and counts.max() == 67
vals, first, rep = np.unique(bill, return_index=True, return_counts=True)
n_repeat = N - len(vals)                                   # dots that sit exactly on an earlier dot
line_y = np.full(N, 2.0)
rank_same = np.arange(N) - np.repeat(first, rep)           # 0 for the first of each value, 1, 2 for its repeats
same_y = 2.0 + 4 * rank_same
b = np.digitize(bill, edges) - 1
rank_bin = np.arange(N) - np.searchsorted(b, b)            # position of each dot inside its bin
bin_x = edges[b] + (rank_bin % PER_ROW + 0.5) * W / PER_ROW
bin_y = (rank_bin // PER_ROW + 0.5) * PER_ROW              # PER_ROW dots per row, so stack height = count


def frame(x, y, title, bins=False, bars=False, opacity=0.45):
    fig = go.Figure()
    if bars:
        fig.add_bar(x=edges[:-1] + W / 2, y=counts, width=W, marker=dict(color=BLUE, opacity=0.35,
                    line=dict(color=BLUE, width=2)), text=counts, textposition="outside", textfont=dict(size=20))
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=9, color=ORANGE, opacity=opacity,
                    line=dict(color="white", width=0.5)))
    if bins:
        for e in edges:
            fig.add_vline(x=e, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False, bargap=0,
                      title=dict(text=title, x=0.5), margin=dict(l=90, r=30, t=80, b=80),
                      xaxis=dict(title="total bill (dollars)", range=[0, 55], dtick=5),
                      yaxis=dict(title="bills in the bin" if bins else "", range=[0, YMAX], showticklabels=bins,
                                 ticks="outside" if bins else ""))
    return fig


if __name__ == "__main__":
    print("repeats:", n_repeat, "counts:", counts)
    figs = [frame(bill, line_y, "<b>244 bills, one dot each</b>: the dots hide each other"),
            frame(bill, same_y, f"<b>Stack equal bills</b>: only {n_repeat} dots move, the rest stay hidden"),
            frame(bill, line_y, "<b>Cut the line into bins</b>, each 5 dollars wide", bins=True)]
    for t in np.linspace(0, 1, 7)[1:]:
        s = t * t * (3 - 2 * t)
        figs.append(frame(bill + s * (bin_x - bill), line_y + s * (bin_y - line_y),
                          "<b>Stack the dots in each bin</b>", bins=True, opacity=0.45 + 0.4 * s))
    figs.append(frame(bin_x, bin_y, "<b>Histogram</b>: bar height = number of bills in the bin", bins=True, bars=True,
                      opacity=0.85))
    save_gif(figs, "dots_to_bins", here, keys=[0, 1, 2, len(figs) - 1], fps=2,
             holds=[5, 5, 4] + [1] * 5 + [3, 10])
