"""Using the 68-95-99.7 rule without a table. The middle 68 percent leaves 32 percent, split by symmetry into two
tails of 16 percent; so the area below z = 1 is 68 + 16 = 84 percent. The same for 2 standard deviations: 95 in the
middle, 2.5 in each tail. Plotly frames -> GIF. Idea after Khan Academy, "ck12.org exercise: Standard normal
distribution and the empirical rule"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, BLUE, ORANGE, GREEN, GREY

here = Path(__file__).parent
z = np.linspace(-4, 4, 801)
y = stats.norm.pdf(z)
assert round(100 * stats.norm.cdf(1)) == 84 and round(100 * stats.norm.sf(2), 1) == 2.3   # the rule's 2.5 is rounded
MID, TAIL = "rgba(245,133,24,0.55)", "rgba(84,162,75,0.6)"


def frame(title, parts, labels):
    """parts: (lo, hi, colour) regions to shade; labels: (x, y, text, colour)."""
    fig = go.Figure()
    for lo, hi, col in parts:
        m = (z >= lo) & (z <= hi)
        fig.add_scatter(x=np.r_[z[m][0], z[m], z[m][-1]], y=np.r_[0, y[m], 0], fill="toself", fillcolor=col,
                        line=dict(width=0), mode="lines")
    fig.add_scatter(x=z, y=y, mode="lines", line=dict(color=BLUE, width=4))
    for x, yy, text, col in labels:
        fig.add_annotation(x=x, y=yy, text=f"<b>{text}</b>", showarrow=False, font=dict(size=30, color=col))
    fig.update_layout(template="simple_white", width=900, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=28), title=dict(text=title, x=0.5, y=0.94),
                      xaxis=dict(title="z", dtick=1), yaxis=dict(title="density", range=[0, 0.45]),
                      margin=dict(l=80, r=30, t=140, b=80))
    return fig


if __name__ == "__main__":
    black = "black"
    figs = [
        frame("<b>Within 1 standard deviation</b><br>the rule gives 68 percent", [(-1, 1, MID)],
              [(0, 0.15, "68", black)]),
        frame("<b>Left over</b>: 100 − 68 = 32 percent<br>two equal tails: 32 / 2 = <b>16 percent each</b>",
              [(-1, 1, MID), (-4, -1, TAIL), (1, 4, TAIL)],
              [(0, 0.15, "68", black), (-2.2, 0.12, "16", GREEN), (2.2, 0.12, "16", GREEN)]),
        frame("<b>Below z = 1</b>: middle + left tail<br>68 + 16 = <b>84 percent</b>",
              [(-4, 1, MID), (1, 4, "rgba(154,154,154,0.25)")],
              [(-0.3, 0.15, "84", black), (2.2, 0.12, "16", GREY)]),
        frame("<b>Within 2 standard deviations</b>: 95 percent<br>left over 5, so <b>2.5 percent in each tail</b>",
              [(-2, 2, MID), (-4, -2, TAIL), (2, 4, TAIL)],
              [(0, 0.15, "95", black), (-2.9, 0.07, "2.5", GREEN), (2.9, 0.07, "2.5", GREEN)]),
    ]
    save_gif(figs, "tails_from_rule", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 4, 4, 6])
