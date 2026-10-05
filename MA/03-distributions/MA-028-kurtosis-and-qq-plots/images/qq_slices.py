"""A Q-Q plot built one point at a time from 15 values: every 10th of the 150 sorted iris sepal lengths.
15 cut lines split a standard normal curve into 16 strips of equal area (wide at the edges, narrow in the
middle); the i-th cut (vertical dotted line) meets the i-th sorted value (horizontal dotted line) at one point.
Plotly frames, because the picture is a curve plus points appearing step by step. -> qq_slices.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.datasets import load_iris
from anim import save_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
DATA = np.sort(load_iris().data[:, 0])[4::10]            # 15 values: 4.5 ... 7.6 cm
N = len(DATA)
Q = stats.norm.ppf(np.arange(1, N + 1) / (N + 1))        # 15 cuts, 16 equal-area strips
assert N == 15 and np.isclose(Q[0], -1.534, atol=1e-3) and np.isclose(Q[2], -0.887, atol=1e-3)
SLOPE, ICPT = np.polyfit(Q, DATA, 1)
xs = np.linspace(-3, 3, 400)


def frame(title, cuts=False, k=0, line=False):
    """k: number of points already placed; the k-th one shows its two dotted lines."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.68, 0.32], vertical_spacing=0.04)
    fig.add_scatter(x=[-2.9] * N, y=DATA, mode="markers", marker=dict(color=BLUE, size=11, symbol="line-ew-open",
                    line_width=3), row=1, col=1)
    fig.add_scatter(x=xs, y=stats.norm.pdf(xs), mode="lines", line=dict(color=ORANGE, width=3), row=2, col=1)
    if cuts:
        edges = np.r_[-3, Q, 3]
        for j in range(N + 1):
            if j % 2 == 0:
                s = np.linspace(edges[j], edges[j + 1], 30)
                fig.add_scatter(x=np.r_[s, s[::-1]], y=np.r_[stats.norm.pdf(s), 0 * s], fill="toself", mode="none",
                                fillcolor="rgba(245,133,24,0.30)", row=2, col=1)
        for q in Q:
            fig.add_scatter(x=[q, q], y=[0, stats.norm.pdf(q)], mode="lines", line=dict(color=ORANGE, width=2),
                            row=2, col=1)
        if k == 0:
            fig.add_annotation(x=-2.3, y=0.2, text="wide strip", showarrow=False, font_size=20, row=2, col=1)
            fig.add_annotation(x=0.9, y=0.47, text="narrow strips", showarrow=False, font_size=20, row=2, col=1)
    if k:
        fig.add_scatter(x=Q[:k], y=DATA[:k], mode="markers", marker=dict(color=BLUE, size=13), row=1, col=1)
        if not line:
            i = k - 1
            fig.add_scatter(x=[-3, Q[i]], y=[DATA[i]] * 2, mode="lines", line=dict(color=BLUE, dash="dot", width=3),
                            row=1, col=1)
            fig.add_scatter(x=[Q[i]] * 2, y=[4.2, DATA[i]], mode="lines", line=dict(color=ORANGE, dash="dot", width=3),
                            row=1, col=1)
            fig.add_scatter(x=[Q[i]] * 2, y=[0, 0.5], mode="lines", line=dict(color=ORANGE, dash="dot", width=3),
                            row=2, col=1)
    if line:
        fig.add_scatter(x=[-2, 2], y=[ICPT - 2 * SLOPE, ICPT + 2 * SLOPE], mode="lines",
                        line=dict(color=RED, width=3), row=1, col=1)
    fig.update_xaxes(range=[-3, 3], row=1, col=1)
    fig.update_xaxes(range=[-3, 3], title_text="normal quantiles (16 strips of equal area)", row=2, col=1)
    fig.update_yaxes(range=[4.2, 7.9], title_text="sepal length (cm)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.52], showticklabels=False, ticks="", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=900, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5), margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame("<b>Step 1</b>: sort the 15 values<br><sup>blue ticks on the vertical axis</sup>"),
            frame("<b>Step 2</b>: cut a normal curve into strips of equal area<br><sup>15 cuts, 16 strips, each "
                  "holds 1/16 of the area</sup>", cuts=True)]
    for i in range(3):
        figs.append(frame(f"<b>Step 3</b>: value {i + 1} meets cut {i + 1}<br><sup>{Q[i]:.2f} across, "
                          f"{DATA[i]:.1f} cm up: one point</sup>", cuts=True, k=i + 1))
    figs.append(frame("<b>Step 3</b>: the same for all 15<br><sup>one point per value</sup>", cuts=True, k=N))
    figs.append(frame("<b>Step 4</b>: draw a straight line<br><sup>points near the line: the shape matches</sup>",
                      cuts=True, k=N, line=True))
    figs[5].data = figs[5].data[:-3]        # all 15 placed: no dotted lines
    save_gif(figs, "qq_slices", here, keys=[1, 2, 4, 6], fps=1, holds=[3, 4, 3, 3, 3, 3, 6], width=640)
    print(DATA, Q.round(2), SLOPE, ICPT)
