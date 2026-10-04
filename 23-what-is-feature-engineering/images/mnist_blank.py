"""Feature selection on MNIST pixels: for each of the 784 pixels, the share of the 70,000 images in which it is
blank (0). Raising the threshold drops more always-blank edge pixels. Data: data/mnist_blank_share.csv, computed
from the Keras copy of MNIST (train + test). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT

here = Path(__file__).parent
b = pd.read_csv(here.parent / "data" / "mnist_blank_share.csv").values[::-1]   # row 0 at the top
assert b.shape == (28, 28) and (b == 1).sum() == 65 and (b >= 0.99).sum() == 290 and (b >= 0.9).sum() == 441
STEPS = [(None, "every pixel is a feature: 784 columns"), (1.0, "drop pixels blank in all 70,000 images"),
         (0.99, "drop pixels blank in at least 99 percent"), (0.9, "drop pixels blank in at least 90 percent")]


def frame(th, words):
    keep = np.ones_like(b, bool) if th is None else b < th
    z = np.where(keep, 1 - b, np.nan)
    fig = go.Figure(go.Heatmap(z=z, colorscale="Blues", zmin=0, zmax=0.6, xgap=1, ygap=1,
                               colorbar=dict(title="share of images<br>where the pixel<br>is not blank",
                                             tickformat=".0%")))
    if th is not None:
        fig.add_heatmap(z=np.where(keep, np.nan, 1), colorscale=[[0, "#e45756"], [1, "#e45756"]], showscale=False,
                        xgap=1, ygap=1, opacity=0.35)
    fig.update_layout(template="simple_white", width=900, height=860, font=FONT,
                      title=dict(text=f"<b>{keep.sum()} pixels kept</b>, {784 - keep.sum()} dropped (red)<br>{words}",
                                 x=0.5, y=0.95),
                      xaxis=dict(visible=False, scaleanchor="y"), yaxis=dict(visible=False),
                      margin=dict(l=20, r=20, t=150, b=20))
    return fig


if __name__ == "__main__":
    save_gif([frame(*s) for s in STEPS], "mnist_blank", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6])
