"""Two inputs competing for each split (Plotly frames -> GIF). Data: data/exam_cgpa.csv (80 students, hours and CGPA,
target marks). For the root and then each of its two children: the best threshold on hours and the best on CGPA are
drawn (dashed), their SSEs compared as bars, and the input with the smaller SSE makes the cut (solid line).
The cuts match the scikit-learn tree of figs.py (max_depth 3, min_samples_leaf 4)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeRegressor
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "exam_cgpa.csv")
X, y = df[["hours", "cgpa"]].to_numpy(), df["marks"].to_numpy()
NAMES = ["hours", "CGPA"]
BOX0 = (0.3, 9.9, 4.9, 10.2)                      # x0, x1, y0, y1 of the whole plane


def best(mask, j, leaf=4):
    """Best threshold on input j inside the node `mask`: (SSE, threshold)."""
    v = np.unique(X[mask, j])
    out = (np.inf, None)
    for t in (v[:-1] + v[1:]) / 2:
        L, R = y[mask & (X[:, j] <= t)], y[mask & (X[:, j] > t)]
        if len(L) < leaf or len(R) < leaf:
            continue
        s = ((L - L.mean()) ** 2).sum() + ((R - R.mean()) ** 2).sum()
        out = min(out, (s, t))
    return out


root = np.ones(len(y), bool)
(sh, th), (sc, tc) = best(root, 0), best(root, 1)
assert sh < sc and round(th, 2) == 2.8
right, left = X[:, 0] > th, X[:, 0] <= th
NODES = [("all 80 students", root, BOX0), (f"students with hours > {th:.1f}", right, (th, BOX0[1], BOX0[2], BOX0[3])),
         (f"students with hours ≤ {th:.1f}", left, (BOX0[0], th, BOX0[2], BOX0[3]))]
sk = DecisionTreeRegressor(max_depth=3, min_samples_leaf=4, random_state=0).fit(X, y).tree_


def cut_line(j, t, box, **line):
    x0, x1, y0, y1 = box
    return dict(type="line", x0=t if j == 0 else x0, x1=t if j == 0 else x1, y0=y0 if j == 0 else t, y1=y1 if j == 0 else t,
                line=line, opacity=1, xref="x", yref="y")


def frames():
    figs, done = [], []
    for name, mask, box in NODES:
        res = [best(mask, 0), best(mask, 1)]
        win = int(res[1][0] < res[0][0])
        for decided in (False, True):
            fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.12,
                                subplot_titles=[name, "SSE of each input's best threshold"])
            fig.update_annotations(font_size=22)
            fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(
                size=11, color=y, colorscale="Blues", cmin=20, cmax=100, line=dict(color="black", width=1),
                opacity=[1.0 if m else 0.25 for m in mask], showscale=False)), 1, 1)
            shapes = [cut_line(j, t, b, color="black", width=4) for j, t, b in done]
            for j in (0, 1):
                if decided and j != win:
                    continue
                shapes.append(cut_line(j, res[j][1], box, color=[BLUE, ORANGE][j], width=5, dash="solid" if decided else "dash"))
            cols = [BLUE, ORANGE] if not decided else [c if j == win else GREY for j, c in enumerate([BLUE, ORANGE])]
            fig.add_trace(go.Bar(x=[f"{NAMES[j]} ≤ {res[j][1]:.2f}" for j in (0, 1)], y=[r[0] for r in res], marker_color=cols,
                                 text=[f"{r[0]:,.0f}" for r in res], textposition="outside", textfont=dict(size=20)), 1, 2)
            title = (f"smaller SSE wins: cut on {NAMES[win]} at {res[win][1]:.2f}" if decided
                     else "best threshold on hours (blue) and on CGPA (orange)")
            fig.update_xaxes(range=[BOX0[0], BOX0[1]], title="hours the day before the exam (darker = higher marks)", row=1, col=1)
            fig.update_yaxes(range=[BOX0[2], BOX0[3]], title="CGPA", row=1, col=1)
            fig.update_yaxes(range=[0, 1.25 * max(r[0] for r in res)], title="SSE", row=1, col=2)
            fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False, shapes=shapes,
                              margin=dict(l=70, r=30, t=120, b=70), title=dict(text=title, x=0.5, y=0.96, font=dict(size=24)))
            figs.append(fig)
        done.append((win, res[win][1], box))
    return figs, done


if __name__ == "__main__":
    figs, done = frames()
    got = sorted((j, round(float(t), 2)) for j, t, _ in done)
    want = sorted((int(sk.feature[n]), round(float(sk.threshold[n]), 2)) for n in (0, sk.children_left[0], sk.children_right[0]))
    assert got == want, (got, want)
    print(got)
    make_gif(figs, here / "two_inputs_race", fps=1, holds=[3, 3, 3, 3, 3, 5], keys=[0, 5], cols=1)
