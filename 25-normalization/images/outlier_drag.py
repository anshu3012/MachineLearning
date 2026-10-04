"""The outlier in the Note's five weights grows from 130 to 1,000. Min-max scaling squeezes the four normal weights
towards 0; robust scaling leaves them exactly where they were. Our own design. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
NORMAL = [32.0, 54, 60, 67]
OUT = [130, 200, 300, 500, 1000]
CLIP = 6.0  # the robust panel stops here; the outlier's true value is printed


def scaled(o):
    w = np.array(NORMAL + [o]).reshape(-1, 1)
    return MinMaxScaler().fit_transform(w).ravel(), RobustScaler().fit_transform(w).ravel()


mm, rb = scaled(130)
assert np.allclose(mm[:4], [0, 0.224, 0.286, 0.357], atol=1e-3) and np.allclose(rb, [-2.154, -0.462, 0, 0.538, 5.385], atol=1e-3)
assert np.allclose(scaled(1000)[1][:4], rb[:4])  # robust: the normal weights do not move


def frame(o):
    mm, rb = scaled(o)
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.34,
                        subplot_titles=[f"Min-max scaling: normal weights in 0 to {mm[3]:.2f}",
                                        f"Robust scaling: normal weights in {rb[0]:.2f} to {rb[3]:.2f}"])
    for r, v, x_out in ((1, mm, mm[4]), (2, rb, min(rb[4], CLIP))):
        fig.add_scatter(x=v[:4], y=[0] * 4, mode="markers", marker=dict(size=22, color=BLUE, opacity=0.85), row=r, col=1)
        fig.add_scatter(x=[x_out], y=[0], mode="markers+text", marker=dict(size=22, color=RED),
                        text=[f"outlier: {v[4]:.3g}" + (" →" if v[4] > CLIP else "")], textposition="top left",
                        textfont=dict(size=20, color=RED), row=r, col=1)
        fig.update_yaxes(visible=False, range=[-0.5, 1.2], row=r, col=1)
    fig.update_xaxes(range=[-0.05, 1.05], row=1, col=1)
    fig.update_xaxes(range=[-2.6, CLIP + 0.3], row=2, col=1)
    fig.update_annotations(font_size=22)
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"<b>Weights 32, 54, 60, 67 and an outlier of {o:,} kg</b>", x=0.5),
                      margin=dict(l=30, r=30, t=120, b=50))
    return fig


if __name__ == "__main__":
    save_gif([frame(o) for o in OUT], "outlier_drag", here, keys=[0, 2, 4], fps=1, holds=[3, 2, 2, 2, 6], cols=1, width=860)
