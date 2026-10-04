"""The known-range case: every pixel of an 8-bit image lies between 0 and 255 before we look at any data, so min-max
scaling is a division by 255. Data: scikit-learn's sample photo china.jpg (all three colour channels).
Our own design. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_sample_image
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
px = load_sample_image("china.jpg").ravel().astype(float)
assert px.min() == 0 and px.max() == 255
counts, edges = np.histogram(px, bins=64, range=(0, 256))
mid = (edges[:-1] + edges[1:]) / 2


def frame(div, head, unit):
    fig = go.Figure(go.Bar(x=mid / div, y=counts, width=4 / div, marker_color=BLUE))
    for v, lab in ((0, "min 0"), (255, "max 255" if div == 1 else "max 1")):
        fig.add_vline(x=v / div, line=dict(color=RED, width=3, dash="dash"), opacity=1)
        fig.add_annotation(x=v / div, y=1.08, yref="paper", text=lab, showarrow=False, font=dict(size=22, color=RED))
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, bargap=0,
                      title=dict(text=f"<b>{head}</b>", x=0.5), xaxis=dict(title=unit, range=[-8 / div, 263 / div]),
                      yaxis=dict(title="number of pixel values"), margin=dict(l=90, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(1, "One photo: every pixel value lies in 0 to 255", "pixel value (8-bit)"),
            frame(255, "Divide by 255: same shape, now 0 to 1", "pixel value / 255")]
    save_gif(figs, "pixel_range", here, keys=[0, 1], fps=1, holds=[3, 6], cols=1, width=860)
