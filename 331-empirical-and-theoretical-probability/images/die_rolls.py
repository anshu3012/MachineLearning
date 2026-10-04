"""A die rolled 10, 1,000 and 100,000 times (the Notebook's draws, seed 7): the share of each face against the
theoretical 1/6. With 10 rolls the face 3 never appears; with 100,000 its share is 0.1662. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
rng = np.random.default_rng(7)
shares = {n: np.bincount(rng.integers(1, 7, n), minlength=7)[1:] / n for n in (10, 1_000, 100_000)}
assert shares[10][2] == 0 and round(shares[100_000][2], 4) == 0.1662


def frame(n):
    s = shares[n]
    fig = go.Figure(go.Bar(x=list(range(1, 7)), y=s, marker_color=[ORANGE if f == 3 else BLUE for f in range(1, 7)],
                           text=[f"{v:.4g}" for v in s], textposition="outside", textfont=dict(size=22)))
    fig.add_hline(y=1 / 6, line=dict(color="black", dash="dash", width=2))
    fig.add_annotation(x=0.5, y=0.4, text="dashed: theory 1/6", showarrow=False, xanchor="left", font=dict(size=24))
    fig.update_layout(template="simple_white", width=900, height=600, font=dict(family="Latin Modern Roman", size=28),
                      title=dict(text=f"<b>{n:,}</b> rolls: empirical P(3) = {s[2]:.4g}", x=0.5),
                      xaxis=dict(title="face", dtick=1), yaxis=dict(title="share of rolls", range=[0, 0.42]),
                      margin=dict(l=90, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in (10, 1_000, 100_000)], "die_rolls", here, keys=[0, 1, 2], fps=1, holds=[4, 4, 6], cols=3)
