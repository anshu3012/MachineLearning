"""Perceptron trick pictures with the line 2x + 3y + 5 = 0 (Plotly):
regions.png - the positive and negative sides; abc.png - changing A, B or C; update.png - one update for each kind of mistake."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
G, B_, R, GREY = "#54A24B", "#4C78A8", "#E45756", "#9A9A9A"
lim = (-6, 6)


def line_xy(a, b, c, lim=lim):
    """Points of ax + by + c = 0 inside the box."""
    if abs(b) > 1e-12:
        x = np.linspace(*lim, 200); return x, -(a * x + c) / b
    return np.full(200, -c / a), np.linspace(*lim, 200)


def fmt(a, b, c):
    co = lambda v: "" if abs(v) == 1 else f"{abs(v):g}"
    s = f"{'−' if a < 0 else ''}{co(a)}x {'+' if b >= 0 else '−'} {co(b)}y {'+' if c >= 0 else '−'} {abs(c):g} = 0"
    return s


def region(fig, a, b, c, row=None, col=None):
    xs = np.linspace(*lim, 121)
    X, Y = np.meshgrid(xs, xs)
    Z = np.sign(a * X + b * Y + c)
    kw = {} if row is None else dict(row=row, col=col)
    fig.add_trace(go.Heatmap(x=xs, y=xs, z=Z, colorscale=[[0, "#DCE6F2"], [1, "#DDEFD9"]], showscale=False,
                             zmin=-1, zmax=1, hoverinfo="skip"), **kw)


# 1. regions
a, b, c = 2, 3, 5
fig = go.Figure()
region(fig, a, b, c)
x, y = line_xy(a, b, c)
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="black", width=4), name=fmt(a, b, c)))
pts = [(2, 1), (-4, -3), (-1, -1)]
for px, py in pts:
    v = a * px + b * py + c
    col = G if v > 0 else (B_ if v < 0 else "#555555")
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers+text", marker=dict(size=13, color=col, line=dict(color="black", width=1)),
                             text=[f"({px}, {py}): 2({px}) + 3({py}) + 5 = {v}".replace("-", "−")], textposition="middle right",
                             textfont=dict(color=col, size=15), showlegend=False))
fig.add_annotation(x=3.5, y=4.5, text="positive side: 2x + 3y + 5 > 0", showarrow=False, font=dict(color=G, size=17))
fig.add_annotation(x=-3, y=-5, text="negative side: 2x + 3y + 5 < 0", showarrow=False, font=dict(color=B_, size=17))
fig.update_layout(template="simple_white", width=760, height=660, font=font, margin=dict(l=60, r=20, t=30, b=60),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="x", range=lim), yaxis=dict(title="y", range=lim, scaleanchor="x"))
fig.write_image(here / "regions.png", scale=2); fig.write_image(here / "regions.pdf")

# 2. changing A, B, C one at a time
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                    subplot_titles=("Change C: the line shifts", "Change A: turns about (0, −5/3)", "Change B: turns about (−5/2, 0)"))
variants = [[(2, 3, 2), (2, 3, 5), (2, 3, 8)], [(0.5, 3, 5), (2, 3, 5), (5, 3, 5)], [(2, 1, 5), (2, 3, 5), (2, 8, 5)]]
cols = ["#F58518", "black", "#B279A2"]
for k, vs in enumerate(variants):
    for (va, vb, vc), colr in zip(vs, cols):
        x, y = line_xy(va, vb, vc)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=colr, width=4 if colr == "black" else 3),
                                 showlegend=False), 1, k + 1)
        j = cols.index(colr)
        fig.add_annotation(x=5.8, y=5.4 - 0.85 * j, text=fmt(va, vb, vc), showarrow=False, xanchor="right",
                           font=dict(color=colr, size=13), bgcolor="rgba(255,255,255,0.9)", row=1, col=k + 1)
    pivot = [None, (0, -5 / 3), (-5 / 2, 0)][k]
    if pivot:
        fig.add_trace(go.Scatter(x=[pivot[0]], y=[pivot[1]], mode="markers", marker=dict(size=11, color=R), showlegend=False), 1, k + 1)
fig.update_xaxes(range=lim, title="x")
fig.update_yaxes(range=lim)
fig.update_yaxes(title="y", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=470, font=font, margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "abc.png", scale=2); fig.write_image(here / "abc.pdf")

# 3. one update for each kind of mistake
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("Negative point (5, 2) on the positive side: subtract", "Positive point (−3, −2) on the negative side: add"))
cases = [((5, 2), B_, -1), ((-3, -2), G, +1)]
for k, ((px, py), colr, sign) in enumerate(cases):
    na, nb, nc = a + sign * px, b + sign * py, c + sign * 1
    region(fig, na, nb, nc, 1, k + 1)
    x, y = line_xy(a, b, c)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=3, dash="dash"), showlegend=False), 1, k + 1)
    x, y = line_xy(na, nb, nc)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="black", width=4), showlegend=False), 1, k + 1)
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=14, color=colr, line=dict(color="black", width=1)),
                             showlegend=False), 1, k + 1)
    fig.add_annotation(x=-5.8, y=5.3, xanchor="left", text=f"old: {fmt(a, b, c)}", showarrow=False, font=dict(color=GREY, size=14),
                       bgcolor="rgba(255,255,255,0.85)", row=1, col=k + 1)
    fig.add_annotation(x=-5.8, y=4.4, xanchor="left", text=f"new: {fmt(na, nb, nc)}", showarrow=False, font=dict(color="black", size=14),
                       bgcolor="rgba(255,255,255,0.85)", row=1, col=k + 1)
    print("case", k, (na, nb, nc), "point value old", a * px + b * py + c, "new", na * px + nb * py + nc)
fig.update_xaxes(range=lim, title="x")
fig.update_yaxes(range=lim)
fig.update_yaxes(title="y", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=560, font=font, margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "update.png", scale=2); fig.write_image(here / "update.pdf")
