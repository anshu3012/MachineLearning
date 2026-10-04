"""The line starts flat at the average package and turns about the mean point of the 160 training students.
Left: the line and every residual (actual - predicted). Right: the sum of squared residuals for each slope tried
so far; the points trace a valley whose lowest point is the best-fit slope, 0.558 (total 16.6).
Plotly frames -> GIF (a curve drawn point by point). Idea after StatQuest, "The Main Ideas of Fitting a Line to Data"."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from common import X_train, y_train, M
from anim import save_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
x, y = X_train["cgpa"].values, y_train.values
xm, ym = x.mean(), y.mean()
ssr = lambda m: float(((y - (ym + m * (x - xm))) ** 2).sum())
assert round(ssr(0), 1) == 73.0 and round(ssr(M), 1) == 16.6
SLOPES = [0, 0.1, 0.2, 0.3, 0.4, 0.5, M, 0.65, 0.75, 0.85, 0.95, 1.05]
grid = np.linspace(-0.02, 1.1, 120)


def frame(i, final=False):
    m = M if final else SLOPES[i]
    seen = SLOPES if final else SLOPES[:i + 1]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.11, subplot_titles=[
        f"package = {m:.2f} × CGPA {'+' if ym - m * xm >= 0 else '−'} {abs(ym - m * xm):.2f}",
        "sum of squared residuals for each slope"])
    for a, b in zip(x, y):
        fig.add_scatter(x=[a, a], y=[b, ym + m * (a - xm)], mode="lines", line=dict(color=RED, width=1.2), opacity=0.6,
                        row=1, col=1)
    fig.add_scatter(x=x, y=y, mode="markers", marker=dict(size=7, color=BLUE), row=1, col=1)
    fig.add_scatter(x=[4, 10], y=[ym + m * (4 - xm), ym + m * (10 - xm)], mode="lines", line=dict(color=ORANGE, width=4),
                    row=1, col=1)
    fig.add_scatter(x=[xm], y=[ym], mode="markers", marker=dict(size=14, color="black", symbol="x"), row=1, col=1)
    if final:
        fig.add_scatter(x=grid, y=[ssr(g) for g in grid], mode="lines", line=dict(color=GREY, width=2), row=1, col=2)
    fig.add_scatter(x=seen, y=[ssr(s) for s in seen], mode="markers", marker=dict(size=11, color=GREY), row=1, col=2)
    fig.add_scatter(x=[m], y=[ssr(m)], mode="markers+text", marker=dict(size=18, color=RED), text=[f"<b>{ssr(m):.1f}</b>"],
                    textposition="top center", textfont=dict(size=24, color=RED), row=1, col=2)
    if final:
        fig.add_annotation(x=M, y=50, showarrow=False, text=f"<b>lowest point: slope {M:.3f}<br>the best-fit line</b>",
                           font=dict(size=21, color=ORANGE), row=1, col=2)
    fig.update_xaxes(title_text="CGPA", range=[4, 10], row=1, col=1)
    fig.update_yaxes(title_text="package (LPA)", range=[0.5, 5.5], row=1, col=1)
    fig.update_xaxes(title_text="slope of the line", range=[-0.08, 1.12], row=1, col=2)
    fig.update_yaxes(title_text="sum of squared residuals", range=[0, 95], row=1, col=2)
    for a in fig.layout.annotations[:2]:
        a.font.size = 22
    fig.update_layout(template="simple_white", width=1300, height=640, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(i) for i in range(len(SLOPES))] + [frame(0, final=True)]
    save_gif(figs, "rotate_valley", here, keys=[0, 3, len(SLOPES) - 1, len(SLOPES)], fps=2,
             holds=[4] + [2] * (len(SLOPES) - 1) + [8], width=900)
