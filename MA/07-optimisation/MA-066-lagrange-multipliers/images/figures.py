"""Plotly figures for the Lagrange multipliers Note.
active_inactive: minimise f = x^2 + 2y^2 with one inequality constraint. Left: x + y >= 3, the constraint is active,
optimum (2, 1) on the boundary, lambda = 4. Right: x + y >= -1, inactive, optimum (0, 0) inside, lambda = 0.
dual_function: the dual of the left problem, D(lambda) = 3 lambda - 3 lambda^2 / 8, below the primal optimum 6
everywhere (weak duality) and touching it at lambda = 4 (strong duality)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=17)

# ---------- active vs inactive
gx, gy = np.linspace(-3, 4, 200), np.linspace(-3, 3, 200)
X, Y = np.meshgrid(gx, gy)
F = X ** 2 + 2 * Y ** 2
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("x + y ≥ 3: active, λ = 4", "x + y ≥ −1: inactive, λ = 0"))
for col, rhs, opt in ((1, 3, (2, 1)), (2, -1, (0, 0))):
    fig.add_trace(go.Contour(x=gx, y=gy, z=F, colorscale="Blues", reversescale=True, showscale=False, opacity=0.5,
                             contours=dict(start=1, end=20, size=2), line=dict(width=1)), 1, col)
    # feasible half-plane x + y >= rhs, clipped to the plot window
    fig.add_trace(go.Scatter(x=[rhs + 3, 4, 4, rhs - 3, rhs + 3], y=[-3, -3, 3, 3, -3], mode="lines", fill="toself",
                             fillcolor="rgba(245,133,24,0.15)", line=dict(width=0), hoverinfo="skip"), 1, col)
    fig.add_trace(go.Scatter(x=[rhs + 3, rhs - 3], y=[-3, 3], mode="lines", line=dict(color=ORANGE, width=3)), 1, col)
    fig.add_trace(go.Scatter(x=[opt[0]], y=[opt[1]], mode="markers",
                             marker=dict(symbol="star", size=20, color=GREEN, line=dict(color="black", width=1))), 1, col)
    fig.add_annotation(x=3.0, y=2.4, text="feasible", showarrow=False, font=dict(color=ORANGE, size=18),
                       bgcolor="white", xref=f"x{col if col > 1 else ''}", yref=f"y{col if col > 1 else ''}")
fig.update_xaxes(range=[-3, 4], title_text="x", constrain="domain")
fig.update_yaxes(range=[-3, 3], title_text="y")
fig.update_yaxes(scaleanchor="x", row=1, col=1)
fig.update_yaxes(scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=480, showlegend=False, font=FONT,
                  margin=dict(l=60, r=20, t=50, b=55))
fig.write_image(here / "active_inactive.png", scale=2)
fig.write_image(here / "active_inactive.pdf")

# ---------- dual function
lam = np.linspace(0, 8, 200)
D = 3 * lam - 3 * lam ** 2 / 8
assert abs(D.max() - 6) < 1e-3 and abs(lam[D.argmax()] - 4) < 0.05
fig = go.Figure()
fig.add_trace(go.Scatter(x=lam, y=D, mode="lines", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=[0, 8], y=[6, 6], mode="lines", line=dict(color=GREY, width=2, dash="dash")))
fig.add_trace(go.Scatter(x=[2, 4], y=[4.5, 6], mode="markers", marker=dict(size=12, color=[ORANGE, GREEN])))
for x, y, t, c, ys, xs in ((2, 4.5, "D(2) = 4.5", ORANGE, -6, 70), (4, 6, "D(4) = 6", GREEN, 22, 0),
                       (6.6, 6, "primal optimum f = 6", GREY, 16, 0), (3.2, 1.0, "dual D(λ) = 3λ − 3λ²/8", BLUE, 0, 0)):
    fig.add_annotation(x=x, y=y, text=t, showarrow=False, yshift=ys, xshift=xs, font=dict(color=c, size=18), bgcolor="white")
fig.update_xaxes(title="λ", range=[0, 8])
fig.update_yaxes(title="value", range=[-1, 7.5])
fig.update_layout(template="simple_white", width=720, height=440, showlegend=False, font=FONT,
                  margin=dict(l=60, r=20, t=20, b=55))
fig.write_image(here / "dual_function.png", scale=2)
fig.write_image(here / "dual_function.pdf")
