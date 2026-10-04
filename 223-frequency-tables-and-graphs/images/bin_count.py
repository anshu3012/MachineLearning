"""The same 714 Titanic ages cut into 2, 8, 20 and 80 bins: the histogram is the frequency table of the bins, and
the number of bins changes what we see. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv").Age.dropna()
assert len(age) == 714
WORDS = {2: "too few, the shape is hidden", 8: "the shape appears", 20: "more detail", 80: "too many, noisy"}


def frame(k):
    edges = np.linspace(0, 80, k + 1)
    n, _ = np.histogram(age, edges)
    assert n.sum() == 714
    fig = go.Figure(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=n, width=np.diff(edges), marker_color=BLUE,
                           marker_line=dict(color="white", width=1 if k < 80 else 0.3)))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, bargap=0,
                      title=dict(text=f"<b>{k} bins</b>, {80 / k:g} year{'s' if k < 80 else ''} wide: {WORDS[k]}", x=0.5),
                      xaxis=dict(title="age (years)", range=[0, 80]), yaxis=dict(title="passengers in the bin"),
                      margin=dict(l=90, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in (2, 8, 20, 80)], "bin_count", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 5])
