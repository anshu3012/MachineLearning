"""The sum of two dice, counted: for each sum, the cells of the 6 x 6 grid of equally likely pairs that give it light
up, and its bar (pairs / 36) is added to the distribution. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
S = np.add.outer(np.arange(1, 7), np.arange(1, 7))          # S[i, j] = (i + 1) + (j + 1)
counts = {s: int((S == s).sum()) for s in range(2, 13)}
assert counts[7] == 6 and counts[2] == counts[12] == 1 and sum(counts.values()) == 36


def frame(k):
    """sums 2..k counted so far (k = 1: nothing yet)."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.1,
                        subplot_titles=["36 equally likely pairs", "P(X = x) = pairs / 36"])
    z = np.where(S == k, 2, np.where(S < k, 1, 0))
    fig.add_heatmap(z=z, x=list(range(1, 7)), y=list(range(1, 7)), showscale=False, xgap=3, ygap=3, zmin=0, zmax=2,
                    colorscale=[[0, "#eeeeee"], [0.5, "#c6d6e8"], [1, ORANGE]], row=1, col=1)
    for i in range(6):
        for j in range(6):
            fig.add_annotation(x=j + 1, y=i + 1, text=str(S[i, j]), showarrow=False, xref="x", yref="y",
                               font=dict(size=20, color="black" if S[i, j] <= k else "#999"))
    xs = list(range(2, 13))
    fig.add_bar(x=xs, y=[counts[s] / 36 if s <= k else 0 for s in xs],
                marker_color=[ORANGE if s == k else BLUE for s in xs],
                text=[f"{counts[s]}/36" if s <= k else "" for s in xs], textposition="outside", row=1, col=2)
    fig.update_xaxes(title_text="first die", tickvals=list(range(1, 7)), row=1, col=1)
    fig.update_yaxes(title_text="second die", tickvals=list(range(1, 7)), scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title_text="sum x", tickvals=xs, range=[1.4, 12.6], row=1, col=2)
    fig.update_yaxes(title_text="probability", range=[0, 0.2], row=1, col=2)
    fig.update_annotations(selector=dict(xref="paper"), font_size=22)
    head = "Two dice: which pairs give each sum?" if k < 2 else f"<b>Sum {k}</b>: {counts[k]} pair{'s' if counts[k] > 1 else ''} → P(X = {k}) = {counts[k]}/36 = {counts[k] / 36:.3f}"
    fig.update_layout(template="simple_white", width=1400, height=640, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=80, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(1, 13)], "dice_grid", here, keys=[1, 3, 6, 11], fps=1,
             holds=[2] + [2] * 10 + [6], width=900)
