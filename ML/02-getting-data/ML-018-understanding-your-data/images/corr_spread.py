"""Section 9.1: r measures how close the points lie to a straight line, not how steep the line is.
Part 1: 40 example points start exactly on a rising line (r = 1) and are spread away from it step by step, down to r = 0.
Part 2: the points sit exactly on a line again while its slope changes; r stays 1.
The points are built as y = r x + sqrt(1 - r^2) z, with z made uncorrelated with x, so the r in each title is the
value np.corrcoef measures on the points drawn. Plotly frames (points moving) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
x = rng.normal(size=40)
x = (x - x.mean()) / x.std()
z = rng.normal(size=40)
z -= z.mean()
z -= (z @ x) / (x @ x) * x                       # remove the part of z that moves with x
z /= z.std()


def frame(y, title, line_slope=None):
    r = np.corrcoef(x, y)[0, 1]
    fig = go.Figure()
    if line_slope is not None:
        fig.add_scatter(x=[-3, 3], y=[-3 * line_slope, 3 * line_slope], mode="lines", line=dict(color="#9A9A9A", width=3), showlegend=False)
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(color="#4C78A8", size=12, opacity=0.85), showlegend=False)
    fig.update_layout(template="simple_white", width=760, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"{title}<br><b>r = {abs(r) if abs(r) < 0.005 else r:.2f}</b>", x=0.5),
                      xaxis=dict(title="feature x", range=[-3, 3], showticklabels=False),
                      yaxis=dict(title="feature y", range=[-3.6, 3.6], showticklabels=False),
                      margin=dict(l=60, r=20, t=110, b=60))
    return fig


if __name__ == "__main__":
    figs = [frame(rho * x + np.sqrt(1 - rho ** 2) * z, t, 1 if rho == 1 else None) for rho, t in
            [(1, "Every point on a rising line"), (0.9, "Points move a little away from the line"),
             (0.7, "Further from the line"), (0.4, "Further still"), (0, "No line left: a blob")]]
    figs += [frame(s * x, t, s) for s, t in [(1, "Back on the line"), (0.3, "A gentle slope: still every point on the line"),
                                             (2.5, "A steep slope: still every point on the line")]]
    save_gif(figs, "corr_spread", HERE, keys=[0, 2, 4, 6, 7], fps=0.8, cols=3)
