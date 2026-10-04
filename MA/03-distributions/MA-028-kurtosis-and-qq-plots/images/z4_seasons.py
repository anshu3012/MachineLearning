"""Kurtosis as the average z^4, for the Note's two 8-match seasons (mean 40, sd 20): season A's eight scores are
each 1 sd away (z^4 = 1, kurtosis 1); season B's two extreme scores have z = +-2 (z^4 = 16) and give kurtosis 4.
Plotly frames: scores -> z -> z^4 -> average."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
A = np.array([20, 20, 20, 20, 60, 60, 60, 60.0]); B = np.array([40, 40, 40, 40, 40, 40, 0, 80.0])
for s, k in ((A, 1), (B, 4)):
    assert s.mean() == 40 and s.std() == 20 and np.isclose(stats.kurtosis(s, fisher=False), k)
STEPS = [("scores", lambda s: s, [0, 90]), ("z-scores (x − 40) / 20", lambda s: (s - 40) / 20, [-2.6, 2.6]),
         ("z⁴", lambda s: ((s - 40) / 20) ** 4, [0, 18])]


def frame(i, avg=False):
    name, f, yr = STEPS[i]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
        "Season A" + (": average z⁴ = 8 / 8 = <b>1</b>" if avg else ""),
        "Season B" + (": average z⁴ = 32 / 8 = <b>4</b>" if avg else "")])
    for j, (s, c) in enumerate(((A, BLUE), (B, ORANGE)), start=1):
        v = f(s)
        fig.add_bar(x=[f"m{k + 1}" for k in range(8)], y=v, marker_color=c, text=[f"{a:g}" for a in v],
                    textposition="outside", textfont=dict(size=20), row=1, col=j)
        fig.update_yaxes(range=yr, row=1, col=j)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"<b>Step {i + 1 + avg}</b>: {name if not avg else 'average the z⁴ values'}", x=0.5),
                      margin=dict(l=60, r=30, t=110, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(0), frame(1), frame(2), frame(2, True)], "z4_seasons", here, keys=[1, 3], fps=1,
             holds=[3, 3, 3, 6], cols=1, width=900)
