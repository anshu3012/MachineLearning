"""Step 5 of the worked example, one feature per frame (Plotly frames -> GIF): the 14 Play Tennis days split by
outlook, humidity, wind and temperature. Each bar is one child, split into yes (green) and no (red), with its entropy;
the title gives the weighted child entropy and the information gain. Outlook wins with 0.247."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
D = [("sunny", "hot", "high", "weak", 0), ("sunny", "hot", "high", "strong", 0), ("overcast", "hot", "high", "weak", 1),
     ("rain", "mild", "high", "weak", 1), ("rain", "cool", "normal", "weak", 1), ("rain", "cool", "normal", "strong", 0),
     ("overcast", "cool", "normal", "strong", 1), ("sunny", "mild", "high", "weak", 0), ("sunny", "cool", "normal", "weak", 1),
     ("rain", "mild", "normal", "weak", 1), ("sunny", "mild", "normal", "strong", 1), ("overcast", "mild", "high", "strong", 1),
     ("overcast", "hot", "normal", "weak", 1), ("rain", "mild", "high", "strong", 0)]
FEATS = {"outlook": 0, "temperature": 1, "humidity": 2, "wind": 3}
y = np.array([d[4] for d in D])


def H(v):
    p = np.bincount(v, minlength=2) / len(v)
    p = p[p > 0]
    return abs(float(-(p * np.log2(p)).sum()))


def gain(f):
    col = np.array([d[FEATS[f]] for d in D])
    kids = {v: y[col == v] for v in dict.fromkeys(col)}
    w = sum(len(k) / len(y) * H(k) for k in kids.values())
    return kids, w, H(y) - w


G = {f: gain(f)[2] for f in FEATS}
assert round(H(y), 3) == 0.940 and {f: round(g, 3) for f, g in G.items()} == {"outlook": 0.247, "humidity": 0.152, "wind": 0.048, "temperature": 0.029}
ORDER = ["outlook", "humidity", "wind", "temperature"]


def frame(k):
    f = ORDER[k]
    kids, w, g = gain(f)
    fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.12,
                        subplot_titles=[f"split on {f}: weighted entropy {w:.3f}", "information gain so far"])
    fig.update_annotations(font_size=21)
    names = list(kids)
    yes = [int(kids[v].sum()) for v in names]; no = [int((1 - kids[v]).sum()) for v in names]
    fig.add_trace(go.Bar(x=names, y=yes, marker_color=GREEN, name="yes", text=yes, textposition="inside", textfont=dict(size=18)), 1, 1)
    fig.add_trace(go.Bar(x=names, y=no, marker_color=RED, name="no", text=no, textposition="inside", textfont=dict(size=18)), 1, 1)
    for v, a, b in zip(names, yes, no):
        fig.add_annotation(x=v, y=a + b, text=f"H = {H(kids[v]):.3f}", showarrow=False, yshift=16, font=dict(size=18), row=1, col=1)
    done = ORDER[:k + 1]
    fig.add_trace(go.Bar(x=done, y=[G[d] for d in done], marker_color=[BLUE if d == "outlook" and k == 3 else GREY for d in done],
                         text=[f"{G[d]:.3f}" for d in done], textposition="outside", textfont=dict(size=18), showlegend=False), 1, 2)
    fig.update_yaxes(title="days", range=[0, 10], row=1, col=1)
    fig.update_yaxes(title="IG = 0.940 − weighted entropy", range=[0, 0.3], row=1, col=2)
    fig.update_xaxes(categoryorder="array", categoryarray=ORDER, range=[-0.5, 3.5], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, barmode="stack",
                      legend=dict(orientation="h", x=0.3, xanchor="center", y=-0.12), margin=dict(l=70, r=30, t=110, b=100),
                      title=dict(text="outlook has the largest gain: it becomes the root" if k == 3 else "", x=0.5, y=0.97))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(4)], here / "gain_race", fps=1, holds=[3, 2, 2, 5], keys=[0, 3], cols=1)
