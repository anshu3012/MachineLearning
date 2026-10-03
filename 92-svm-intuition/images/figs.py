"""Note 92 figures (Plotly): two_lines.png - two lines that both separate the classes;
margins.png - the margin d of each line, found with the parallel lines pi+ and pi-."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=20)
GREEN, RED, BLUE, GREY = "#54A24B", "#E45756", "#4C78A8", "#6B6B6B"
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
xs = np.array([0, 8.5])

# pi: the widest-margin line (scikit-learn with a huge C behaves like the hard-margin SVM)
svm = SVC(kernel="linear", C=1e6).fit(X, y)
w_pi, b_pi = svm.coef_[0], svm.intercept_[0]
w_dash, b_dash = np.array([0.3, 1.0]), -6.3          # pi': y = 6.3 - 0.3x, also separates the classes


def line(w, b, shift=0.0):
    """y values of w.x + b = shift along xs."""
    return (shift - b - w[0] * xs) / w[1]


def margin(w, b):
    """Slide parallel lines to the first green and the first red point: returns their offsets and the margin d."""
    n = np.linalg.norm(w)
    top, bottom = (G @ w + b).min(), (R @ w + b).max()          # values of w.x + b at the touching points
    return top, bottom, (top - bottom) / n


def points(fig, **rc):
    fig.add_trace(go.Scatter(x=G[:, 0], y=G[:, 1], mode="markers", name="green class",
                             marker=dict(color=GREEN, size=12, line=dict(color="black", width=1)), showlegend=not rc), **rc)
    fig.add_trace(go.Scatter(x=R[:, 0], y=R[:, 1], mode="markers", name="red class",
                             marker=dict(color=RED, size=12, line=dict(color="black", width=1)), showlegend=not rc), **rc)


axes = dict(xaxis=dict(title="x₁", range=[0, 8.5]), yaxis=dict(title="x₂", range=[0, 10], scaleanchor="x"))

# 1. two lines, both 100% accurate
fig = go.Figure()
points(fig)
fig.add_trace(go.Scatter(x=xs, y=line(w_pi, b_pi), mode="lines", line=dict(color="black", width=4), name="π₁"))
fig.add_trace(go.Scatter(x=xs, y=line(w_dash, b_dash), mode="lines", line=dict(color=BLUE, width=4), name="π₂"))
fig.update_layout(template="simple_white", width=640, height=560, font=font, margin=dict(l=60, r=20, t=50, b=60),
                  title=dict(text="Both lines classify every training point correctly", x=0.5),
                  legend=dict(x=1.02, y=0.5), **axes)
fig.write_image(here / "two_lines.png", scale=2); fig.write_image(here / "two_lines.pdf")

# 2. the margin of each line
titles = [f"π₁: margin d = {margin(w_pi, b_pi)[2]:.2f}", f"π₂: margin d′ = {margin(w_dash, b_dash)[2]:.2f}"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=titles)
for k, (w, b, colour, name) in enumerate([(w_pi, b_pi, "black", "π₁"), (w_dash, b_dash, BLUE, "π₂")], start=1):
    top, bottom, d = margin(w, b)
    points(fig, row=1, col=k)
    fig.add_trace(go.Scatter(x=xs, y=line(w, b), mode="lines", line=dict(color=colour, width=4), showlegend=False), 1, k)
    for shift in (top, bottom):
        fig.add_trace(go.Scatter(x=xs, y=line(w, b, shift), mode="lines", showlegend=False,
                                 line=dict(color=GREY, width=2.5, dash="dash")), 1, k)
    touch = np.r_[G[np.isclose(G @ w + b, top, atol=1e-3)], R[np.isclose(R @ w + b, bottom, atol=1e-3)]]
    fig.add_trace(go.Scatter(x=touch[:, 0], y=touch[:, 1], mode="markers", showlegend=False,
                             marker=dict(size=26, color="rgba(0,0,0,0)", line=dict(color="black", width=2.5))), 1, k)
    # double arrow across the margin, perpendicular to the lines, at x = 0.9 on the lower line
    unit = w / np.linalg.norm(w)
    start = np.array([0.9, (bottom - b - w[0] * 0.9) / w[1]])
    end = start + unit * d
    fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1], xref=f"x{k}", yref=f"y{k}", axref=f"x{k}",
                       ayref=f"y{k}", showarrow=True, arrowhead=2, arrowside="end+start", arrowwidth=2.5, text="")
    fig.add_annotation(x=8.3, y=line(w, b, top)[1] + 0.45, text=f"{name}+", showarrow=False, xanchor="right",
                       font=dict(color=GREY, size=16), row=1, col=k)
    fig.add_annotation(x=8.3, y=line(w, b, bottom)[1] - 0.45, text=f"{name}−", showarrow=False, xanchor="right",
                       font=dict(color=GREY, size=16), row=1, col=k)
    print(name, "margin", round(d, 3))
fig.update_xaxes(title="x₁", range=[0, 8.5])
fig.update_yaxes(range=[0, 10])
fig.update_yaxes(title="x₂", row=1, col=1)
fig.update_yaxes(scaleanchor="x", row=1, col=1)
fig.update_yaxes(scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1000, height=560, font=font, margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "margins.png", scale=2); fig.write_image(here / "margins.pdf")
