"""Building a residual plot by hand on four made-up points (1, 2), (2, 3), (3, 7), (4, 8). Their least-squares line
is y = 2.2x - 0.5, so the residuals are +0.3, -0.9, +0.9, -0.3. Left: the points, the line and each residual as a
stick. Right: the same sticks moved onto a flat zero line, one at a time: the residual plot.
Plotly frames -> GIF. Idea after Khan Academy, "Residual plots"."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from gifkit import make_gif, FONT, BLUE, ORANGE, GREEN, RED, GREY

here = Path(__file__).parent
x, y = np.array([1, 2, 3, 4.0]), np.array([2, 3, 7, 8.0])
m, b = np.polyfit(x, y, 1)
pred = m * x + b
res = y - pred
assert (round(m, 2), round(b, 2)) == (2.2, -0.5) and list(res.round(2)) == [0.3, -0.9, 0.9, -0.3]
colour = lambda r: GREEN if r > 0 else RED


def frame(k, final=False):
    """k residuals already moved to the right panel (0 to 4)."""
    head = ("4 points and their least-squares line" if k == 0 else
            "the residual plot: residuals around a flat zero line" if final else
            f"x = {x[k - 1]:.0f}: residual = {y[k - 1]:.0f} − {pred[k - 1]:.1f} = {res[k - 1]:+.1f}")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=["data and line  ŷ = 2.2x − 0.5", "residual plot"])
    fig.add_scatter(x=[0.5, 4.5], y=[m * 0.5 + b, m * 4.5 + b], mode="lines", line=dict(color=ORANGE, width=4), row=1, col=1)
    fig.add_scatter(x=[0.5, 4.5], y=[0, 0], mode="lines", line=dict(color=ORANGE, width=4), row=1, col=2)
    for i in range(4):
        hot = (i == k - 1) and not final
        w = 7 if hot else 4
        fig.add_scatter(x=[x[i], x[i]], y=[pred[i], y[i]], mode="lines", line=dict(color=colour(res[i]), width=w),
                        opacity=1 if i >= k - 1 or final else 0.45, row=1, col=1)
        if i < k:
            fig.add_scatter(x=[x[i], x[i]], y=[0, res[i]], mode="lines+markers+text", line=dict(color=colour(res[i]), width=w),
                            marker=dict(size=[0, 14], color=BLUE), text=["", f"{res[i]:+.1f}"],
                            textposition="top center" if res[i] > 0 else "bottom center",
                            textfont=dict(size=22, color=colour(res[i])), row=1, col=2)
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=14, color=BLUE), row=1, col=1)
    fig.update_xaxes(title_text="x", range=[0.4, 4.6], dtick=1)
    fig.update_yaxes(title_text="y", range=[0, 9.5], row=1, col=1)
    fig.update_yaxes(title_text="residual = actual − predicted", range=[-1.6, 1.6], row=1, col=2)
    for a in fig.layout.annotations[:2]:
        a.font.size = 22
        a.y = 1.0
    fig.update_layout(template="simple_white", width=1300, height=640, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, font=dict(size=26)), margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(5)] + [frame(4, final=True)]
    make_gif(figs, here / "residual_plot_build", fps=1, holds=[3, 2, 2, 2, 2, 6], keys=[2, 5], cols=1, width=900)
