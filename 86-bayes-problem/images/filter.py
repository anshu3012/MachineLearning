"""Bayes' theorem as filtering (Plotly frames -> GIF), with the expected counts of a batch of 1000 markers: 200 from
M1, 300 from M2, 500 from M3; 10, 9 and 5 of them defective (5%, 3%, 1%). Frame 1: the whole batch, one square
per marker. Frame 2: the 24 defective markers lit up. Frame 3: only the defective markers are left; 10, 9 and 5 of
24 give the posteriors 0.417, 0.375 and 0.208."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif

here = Path(__file__).parent
N, share, rate = 1000, [0.2, 0.3, 0.5], [0.05, 0.03, 0.01]
n = [round(N * s) for s in share]
d = [round(k * r) for k, r in zip(n, rate)]
assert n == [200, 300, 500] and d == [10, 9, 5] and [round(x / sum(d), 3) for x in d] == [0.417, 0.375, 0.208]
COLS, NAMES = [BLUE, ORANGE, GREEN], ["M1", "M2", "M3"]
W = 40                                                  # 40 columns x 25 rows
mach = np.repeat([0, 1, 2], n)
defect = np.concatenate([np.r_[np.ones(dk), np.zeros(nk - dk)] for nk, dk in zip(n, d)]).astype(bool)
rng = np.random.default_rng(3)
for k in range(3):                                      # spread each machine's defects through its block
    idx = np.flatnonzero(mach == k)
    defect[idx] = rng.permutation(defect[idx])
cx, cy = np.arange(N) % W, -(np.arange(N) // W)


def frame(step):
    fig = go.Figure()
    if step < 3:
        for k in range(3):
            m = mach == k
            op = np.where(defect[m], 1.0, 1.0 if step == 1 else 0.12)
            fig.add_scatter(x=cx[m], y=cy[m], mode="markers", name=f"{NAMES[k]}: {n[k]} markers, {d[k]} defective",
                            marker=dict(symbol="square", size=13, color=COLS[k], opacity=op,
                                        line=dict(color="black", width=np.where(defect[m] & (step == 2), 2.5, 0))))
        title = ("a batch of 1000 markers, coloured by machine" if step == 1 else
                 "the 24 defective markers lit up: the evidence D")
        fig.update_xaxes(visible=False, range=[-1, W]); fig.update_yaxes(visible=False, range=[-26, 1])
    else:
        x0 = 0
        for k in range(3):
            fig.add_scatter(x=list(range(x0, x0 + d[k])), y=[0] * d[k], mode="markers", name=f"{NAMES[k]}: {d[k]} of 24 = {d[k] / 24:.3f}",
                            marker=dict(symbol="square", size=34, color=COLS[k], line=dict(color="black", width=2)))
            fig.add_annotation(x=x0 + (d[k] - 1) / 2, y=0.6, text=f"{NAMES[k]}<br>{d[k] / 24:.3f}", showarrow=False,
                               font=dict(size=22, color=COLS[k]))
            x0 += d[k] + 1
        title = "given D, only the 24 defective markers remain: the posteriors"
        fig.update_xaxes(visible=False, range=[-1, 27]); fig.update_yaxes(visible=False, range=[-0.5, 1.0])
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02), margin=dict(l=20, r=20, t=70, b=80))
    return fig


if __name__ == "__main__":
    make_gif([frame(s) for s in (1, 2, 3)], here / "filter", fps=1, holds=[3, 3, 5], keys=[1, 2], cols=2, width=800)
