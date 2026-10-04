"""Still figures for the 2-2-1 regression network and student 1 (x = (8, 8), y = 4) (Plotly):
knobs.png (section 3), bowl.png (section 6), slope_sign.png (section 7), convergence.png (section 9)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
F = dict(FONT, size=20)
x, y = np.array([8.0, 8.0]), 4.0
START = dict(W111=0.1, W121=0.1, W112=0.1, W122=0.1, b11=0.0, b12=0.0, W211=0.1, W221=0.1, b21=0.0)
NAMES = dict(W111="W¹₁₁", W121="W¹₂₁", W112="W¹₁₂", W122="W¹₂₂", b11="b₁₁", b12="b₁₂", W211="W²₁₁", W221="W²₂₁", b21="b₂₁")


def loss(p):
    O11 = p["W111"] * x[0] + p["W121"] * x[1] + p["b11"]
    O12 = p["W112"] * x[0] + p["W122"] * x[1] + p["b12"]
    return (y - (p["W211"] * O11 + p["W221"] * O12 + p["b21"])) ** 2


assert round(loss(START), 2) == 13.54

# Section 3: turn one parameter, freeze the other eight
fig = make_subplots(rows=3, cols=3, subplot_titles=[f"turn {NAMES[k]}" for k in START], vertical_spacing=0.12,
                    horizontal_spacing=0.07)
for i, k in enumerate(START):
    v = np.linspace(START[k] - 4, START[k] + 4, 200)
    Lv = [loss({**START, k: t}) for t in v]
    c = BLUE if k.startswith("W1") or k in ("b11", "b12") else ORANGE
    fig.add_trace(go.Scatter(x=v, y=Lv, line=dict(color=c, width=4), showlegend=False), row=i // 3 + 1, col=i % 3 + 1)
    fig.add_trace(go.Scatter(x=[START[k]], y=[loss(START)], mode="markers", marker=dict(color=RED, size=11),
                             showlegend=False), row=i // 3 + 1, col=i % 3 + 1)
fig.update_yaxes(range=[0, 40], dtick=20)
fig.update_layout(template="simple_white", width=1100, height=820, font=F, margin=dict(l=50, r=20, t=50, b=40))
fig.update_annotations(font_size=22)
fig.write_image(here / "knobs.png", scale=2)

# Section 6: z = x^2 + y^2, both slopes zero only at (0, 0)
g = np.linspace(-3, 3, 121)
fig = go.Figure(go.Contour(x=g, y=g, z=g[None, :] ** 2 + g[:, None] ** 2, colorscale="Blues", showscale=False,
                           contours=dict(start=1, end=17, size=2, showlabels=True, labelfont=dict(size=16)), opacity=0.8))
for (px, py), c in (((2, 1), ORANGE), ((-1, 2), ORANGE), ((-2, -1.5), ORANGE)):
    gx, gy = 2 * px, 2 * py                                  # the two partial derivatives
    fig.add_annotation(x=px - 0.25 * gx, y=py - 0.25 * gy, ax=px, ay=py, axref="x", ayref="y", showarrow=True,
                       arrowhead=3, arrowwidth=3, arrowcolor=c, text="")
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers+text", marker=dict(color=c, size=12), showlegend=False,
                             text=[f"slopes ({gx:g}, {gy:g})"], textposition="bottom center" if py < 0 else "top center", textfont=dict(size=18, color=c)))
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", marker=dict(color=RED, size=18, symbol="star"),
                         text=["minimum: slopes (0, 0)"], textposition="bottom center", textfont=dict(size=20, color=RED),
                         showlegend=False))
fig.update_layout(template="simple_white", width=760, height=700, font=F, xaxis=dict(title="x"),
                  yaxis=dict(title="y", scaleanchor="x"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "bowl.png", scale=2)

# Section 7: the sign of the slope picks the direction
b = np.linspace(-7, 9, 400)
L = lambda t: (3.68 - t) ** 2
dL = lambda t: -2 * (3.68 - t)
assert round(dL(-5), 2) == -17.36 and round(dL(5), 2) == 2.64
fig = go.Figure(go.Scatter(x=b, y=L(b), line=dict(color=GREY, width=4), name="L(b₂₁) = (3.68 − b₂₁)²"))
for b0, c, txt in ((-5, BLUE, "slope −17.36 < 0<br>update adds: move right"), (5, ORANGE, "slope +2.64 > 0<br>update subtracts: move left")):
    t = np.linspace(b0 - 1.6, b0 + 1.6, 2)
    fig.add_trace(go.Scatter(x=t, y=L(b0) + dL(b0) * (t - b0), mode="lines", line=dict(color=c, width=3, dash="dash"),
                             showlegend=False))
    fig.add_trace(go.Scatter(x=[b0], y=[L(b0)], mode="markers", marker=dict(color=c, size=14), showlegend=False))
    step = -np.sign(dL(b0)) * 2.4
    fig.add_annotation(x=b0 + step, y=L(b0) + 12, ax=b0, ay=L(b0) + 12, axref="x", ayref="y", xref="x", yref="y",
                       showarrow=True, arrowhead=3, arrowwidth=4, arrowcolor=c, text="")
    fig.add_annotation(x=b0 + (3.6 if b0 < 0 else 0), y=L(b0) + (8 if b0 < 0 else 28), text=txt, showarrow=False,
                       font=dict(color=c, size=20), xanchor="left" if b0 < 0 else "center")
fig.add_trace(go.Scatter(x=[3.68], y=[0], mode="markers+text", text=["minimum 3.68"], textposition="bottom center",
                         marker=dict(color=RED, size=13, symbol="star"), showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=520, font=F, xaxis=dict(title="b₂₁"),
                  yaxis=dict(title="loss", range=[-12, 105]), legend=dict(x=0.35, y=0.98), margin=dict(l=70, r=30, t=30, b=60))
fig.write_image(here / "slope_sign.png", scale=2)

# Section 9: with eta = 0.1 the change per update shrinks towards 0 as b21 reaches 3.68
bs = [-5.0]
for _ in range(40):
    bs.append(bs[-1] - 0.1 * dL(bs[-1]))
bs = np.array(bs)
step = np.abs(np.diff(bs))
assert round(bs[1], 3) == -3.264 and round(bs[10], 2) == 2.75 and np.allclose(step[1:] / step[:-1], 0.8)
assert round(step[0], 1) == 1.7 and round(step[-1], 4) == 0.0003          # Section 9 text
fig = make_subplots(rows=1, cols=2, subplot_titles=("b₂₁ after each update", "size of the change, |new b₂₁ − old b₂₁|"),
                    horizontal_spacing=0.13)
fig.add_trace(go.Scatter(x=np.arange(41), y=bs, mode="lines+markers", line=dict(color=GREEN, width=3), showlegend=False), 1, 1)
fig.add_hline(y=3.68, line=dict(color=RED, dash="dash", width=2), row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(1, 41), y=step, mode="lines+markers", line=dict(color=BLUE, width=3), showlegend=False), 1, 2)
fig.update_yaxes(type="log", dtick=1, exponentformat="power", row=1, col=2)
fig.update_xaxes(title_text="update", row=1, col=1)
fig.update_xaxes(title_text="update", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=F, margin=dict(l=70, r=30, t=60, b=60))
fig.update_annotations(font_size=22)
fig.write_image(here / "convergence.png", scale=2)
print("step after 40 updates:", step[-1])
