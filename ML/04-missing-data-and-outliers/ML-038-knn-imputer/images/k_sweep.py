"""The k nearest neighbours of row 2 in the Note's five-row example, laid out by their nan-Euclidean distance from
row 2 (3.46, 7.14, 8.66, 30.62). For k = 1 to 4 the k closest rows light up and their f1 values are averaged:
25, 32.5, 31.67, 36.25. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.impute import KNNImputer
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
X = np.array([[30, 60, np.nan], [np.nan, 55, 20], [40, 52, 25], [25, np.nan, 22], [50, 70, 40]])
D = {1: 8.66, 3: 7.14, 4: 3.46, 5: 30.62}
F1 = {1: 30, 3: 40, 4: 25, 5: 50}
order = sorted(D, key=D.get)
for k, want in ((1, 25), (2, 32.5), (3, 31.67), (4, 36.25)):
    got = KNNImputer(n_neighbors=k).fit_transform(X)[1, 0]
    assert round(got, 2) == want, (k, got)


def frame(k):
    near = order[:k]
    fig = go.Figure()
    fig.add_shape(type="line", x0=0, x1=33, y0=0, y1=0, line=dict(color="#bbbbbb", width=2))
    fig.add_scatter(x=[0], y=[0], mode="markers+text", text=["row 2<br>f1 = ?"], textposition="bottom center",
                    marker=dict(size=26, color="#E45756"), textfont=dict(size=19))
    for r in order:
        on = r in near
        fig.add_scatter(x=[D[r]], y=[0], mode="markers+text", text=[f"row {r}<br>f1 = {F1[r]}<br>d = {D[r]}"],
                        textposition="bottom center" if r == 3 else "top center", marker=dict(size=24, color=ORANGE if on else BLUE, opacity=1 if on else 0.4),
                        textfont=dict(size=17, color="black" if on else "#888"))
    vals = [F1[r] for r in near]
    head = (f"<b>k = {k}</b>: fill = " + (f"<b>{vals[0]}</b>, the value of the single nearest row" if k == 1 else f"({' + '.join(map(str, vals))}) / {k} = <b>{np.mean(vals):.4g}</b>"))
    fig.update_layout(template="simple_white", width=1200, height=380, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), xaxis=dict(title="nan-Euclidean distance from row 2", range=[-2, 34]),
                      yaxis=dict(visible=False, range=[-1.2, 1.6]), margin=dict(l=30, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(1, 5)], "k_sweep", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6], cols=1, width=900)
