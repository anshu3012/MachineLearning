"""The ice-cream sales story (Plotly).
1. outer_product.gif: the plan table built row by row: row i = shop size u_i times the day row v = [2, 2, 4, 6].
2. sales_layers.png: the real table S (large shop sold one extra box on Saturday and Sunday) = layer 1 + layer 2 of
   its SVD; sigma_1 = 30.03, sigma_2 = 0.33; layer 1 rounded to whole boxes gives S back.
3. unit_stretch.png: A = [[3, 0], [4, 5]] sends the unit circle to an ellipse; longest arrow sigma_1 = 6.71,
   shortest sigma_2 = 2.24 (the spectral norm is the longest).
Run: python sales_figures.py"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

HERE = Path(__file__).parent
SHOPS, DAYS = ["small", "medium", "large"], ["Mon", "Tue", "Sat", "Sun"]
u, v = np.array([1, 2, 3]), np.array([2, 2, 4, 6])
P = np.outer(u, v)
S = P.astype(float)
S[2, 2:] += 1                                     # large shop: one extra box on Saturday and Sunday
U, s, Vt = np.linalg.svd(S)
L1, L2 = s[0] * np.outer(U[:, 0], Vt[0]), s[1] * np.outer(U[:, 1], Vt[1])
assert round(s[0], 2) == 30.03 and round(s[1], 2) == 0.33 and np.array_equal(np.round(L1), S)


def table(fig, z, text, row, col, colorscale, zmin, zmax, hl=None):
    fig.add_trace(go.Heatmap(z=z, x=DAYS, y=SHOPS, colorscale=colorscale, zmin=zmin, zmax=zmax, showscale=False,
                             text=text, texttemplate="%{text}", textfont=dict(size=26), xgap=3, ygap=3), row, col)
    fig.update_yaxes(autorange="reversed", row=row, col=col)
    if hl is not None:
        fig.add_shape(type="rect", x0=-0.5, x1=3.5, y0=hl - 0.5, y1=hl + 0.5, line=dict(color=RED, width=5),
                      fillcolor="rgba(0,0,0,0)", layer="above", row=row, col=col)


# 1. outer product animation
def op_frame(k):
    """k rows filled (0..3)."""
    z = np.full(P.shape, np.nan)
    z[:k] = P[:k]
    text = [[str(P[i, j]) if i < k else "" for j in range(4)] for i in range(3)]
    if k == 0:
        title = "plan = shop size × day busyness"
    elif k <= 3:
        r = P[k - 1]
        title = f"row {k} = {u[k - 1]} × [2, 2, 4, 6] = [{', '.join(map(str, r))}]"
    fig = make_subplots(1, 2, column_widths=[0.16, 0.84], horizontal_spacing=0.06,
                        subplot_titles=["shop size u", "boxes sold (day busyness v on top)"])
    fig.add_trace(go.Heatmap(z=u[:, None], y=SHOPS, x=["u"], colorscale="Oranges", zmin=0, zmax=4, showscale=False,
                             text=u[:, None].astype(str), texttemplate="%{text}", textfont=dict(size=26),
                             xgap=3, ygap=3), 1, 1)
    fig.update_yaxes(autorange="reversed", row=1, col=1)
    table(fig, z, text, 1, 2, "Blues", 0, 20, hl=(k - 1) if 1 <= k <= 3 else None)
    fig.update_xaxes(ticktext=[f"{d}<br>{x}" for d, x in zip(DAYS, v)], tickvals=DAYS, side="top", row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, showlegend=False,
                      margin=dict(l=110, r=20, t=170, b=40),
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font=dict(size=28)))
    fig.update_annotations(font_size=22, yshift=58)
    return fig


figs = [op_frame(k) for k in range(4)]
last = op_frame(3)
last.update_layout(title=dict(text="<b>12 numbers described by 3 + 4 = 7 numbers</b>"))
last.layout.shapes = ()
figs.append(last)
make_gif(figs, HERE / "outer_product.gif", fps=2, holds=[3, 4, 4, 4, 8], keys=[1, 4], width=800)

# 2. real table = layer 1 + layer 2
fig = make_subplots(1, 3, horizontal_spacing=0.07, subplot_titles=[
    "real sales S", f"layer 1 (σ<sub>1</sub> = {s[0]:.2f})", f"layer 2 (σ<sub>2</sub> = {s[1]:.2f})"])
table(fig, S, S.astype(int).astype(str), 1, 1, "Blues", 0, 20)
table(fig, L1, np.vectorize(lambda x: f"{x:.2f}")(L1), 1, 2, "Blues", 0, 20)
lim = np.abs(L2).max()
table(fig, L2, np.vectorize(lambda x: "0.00" if abs(x) < 0.005 else f"{x:+.2f}")(L2), 1, 3, "RdBu", -lim * 1.6, lim * 1.6)
for c in (2, 3):
    fig.update_yaxes(showticklabels=False, row=1, col=c)
fig.update_xaxes(side="top")
fig.add_annotation(text="=", x=0.315, y=0.45, xref="paper", yref="paper", showarrow=False, font=dict(size=48))
fig.add_annotation(text="+", x=0.66, y=0.45, xref="paper", yref="paper", showarrow=False, font=dict(size=48))
fig.update_layout(template="simple_white", width=1500, height=430, font=FONT, showlegend=False,
                  margin=dict(l=110, r=20, t=120, b=20))
fig.update_annotations(selector=dict(text="real sales S"), yshift=40)
for a in fig.layout.annotations[:3]:
    a.update(yshift=40, font=dict(size=26))
fig.write_image(HERE / "sales_layers.png", scale=2)
fig.write_image(HERE / "sales_layers.pdf")

# 3. A stretches the unit circle
A = np.array([[3, 0], [4, 5]])
Ua, sa, Vta = np.linalg.svd(A)
t = np.linspace(0, 2 * np.pi, 300)
circ = np.vstack([np.cos(t), np.sin(t)])
ell = A @ circ
fig = make_subplots(1, 2, horizontal_spacing=0.1,
                    subplot_titles=["inputs: unit arrows (length 1)", "outputs: A times each arrow"])
fig.add_trace(go.Scatter(x=circ[0], y=circ[1], mode="lines", line=dict(color=GREY, width=3)), 1, 1)
fig.add_trace(go.Scatter(x=ell[0], y=ell[1], mode="lines", line=dict(color=BLUE, width=3)), 1, 2)
for i, col in [(0, ORANGE), (1, GREEN)]:
    vv = Vta[i] * np.sign(Vta[i].sum() + 1e-9 * (i - 0.5))
    av = A @ vv
    for c, (p, lab) in enumerate([(vv, f"v<sub>{i + 1}</sub>"), (av, f"length {sa[i]:.2f}")], start=1):
        ax = "" if c == 1 else "2"
        fig.add_annotation(x=p[0], y=p[1], ax=0, ay=0, xref=f"x{ax}", yref=f"y{ax}", axref=f"x{ax}", ayref=f"y{ax}",
                           showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=col, text="")
        fig.add_annotation(x=p[0], y=p[1], text=lab, showarrow=False, xref=f"x{ax}", yref=f"y{ax}",
                           font=dict(color=col, size=24), xshift=55 if i == 0 else -60, yshift=12)
assert round(sa[0], 2) == 6.71 and round(sa[1], 2) == 2.24
fig.update_xaxes(range=[-1.6, 1.6], row=1, col=1)
fig.update_yaxes(range=[-1.6, 1.6], scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[-7.5, 7.5], row=1, col=2)
fig.update_yaxes(range=[-7.5, 7.5], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False,
                  margin=dict(l=50, r=20, t=60, b=40))
fig.update_annotations(selector=dict(showarrow=False), font_size=24)
fig.write_image(HERE / "unit_stretch.png", scale=2)
fig.write_image(HERE / "unit_stretch.pdf")
