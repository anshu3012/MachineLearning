"""Note 94 figures (Plotly): slack.png - the slack xi of each point that breaks its constraint;
c_effect.png - large C (narrow margin, no mistakes) vs small C (wide margin, some mistakes); hinge.png - hinge loss vs log loss."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=18)
GREEN, RED, BLUE, ORANGE, GREY = "#54A24B", "#E45756", "#4C78A8", "#F58518", "#6B6B6B"
# the data of the SVM intuition Note plus two points on the wrong side
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8), (6, 4.3)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5), (2.8, 5.2)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
xs = np.array([0, 8.5])


def fit(C):
    m = SVC(kernel="linear", C=C).fit(X, y)
    return m.coef_[0], m.intercept_[0]


def draw(fig, w, b, **rc):
    for rhs, colour, dash, name in ((0, "black", "solid", "π"), (1, GREEN, "dash", "π+"), (-1, RED, "dash", "π−")):
        fig.add_trace(go.Scatter(x=xs, y=(rhs - b - w[0] * xs) / w[1], mode="lines", name=name, showlegend=False,
                                 line=dict(color=colour, width=4 if rhs == 0 else 3, dash=dash)), **rc)
    for P, c in ((G, GREEN), (R, RED)):
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", showlegend=False,
                                 marker=dict(color=c, size=12, line=dict(color="black", width=1))), **rc)


def xi(w, b):
    return np.maximum(0, 1 - y * (X @ w + b))


axes = dict(range=[0, 8.5])

# 1. slack of each point, for C = 1
w, b = fit(1)
s = xi(w, b)
n = np.linalg.norm(w)
fig = go.Figure()
draw(fig, w, b)
for i in np.flatnonzero(s > 1e-6):
    # walk from the point towards its own hyperplane: a distance of xi / |w| along y_i * w
    end = X[i] + y[i] * s[i] / n * w / n
    fig.add_trace(go.Scatter(x=[X[i, 0], end[0]], y=[X[i, 1], end[1]], mode="lines", showlegend=False,
                             line=dict(color=ORANGE, width=4)))
    fig.add_annotation(x=X[i, 0] + 0.25, y=(X[i, 1] + end[1]) / 2, xanchor="left", showarrow=False,
                       text=f"ξ = {s[i]:.2f}", font=dict(size=18, color=ORANGE), bgcolor="rgba(255,255,255,0.85)")
    print("point", X[i], "label", y[i], "xi", round(s[i], 3))
for rhs, txt, c in ((1, "π+", GREEN), (0, "π", "black"), (-1, "π−", RED)):
    fig.add_annotation(x=8.4, y=(rhs - b - w[0] * 8.4) / w[1] + 0.35, text=txt, showarrow=False, xanchor="right",
                       font=dict(color=c, size=18))
fig.update_layout(template="simple_white", width=480, height=520, font=font, margin=dict(l=60, r=20, t=40, b=60),
                  xaxis=dict(title="x₁", **axes), yaxis=dict(title="x₂", range=[0, 10], scaleanchor="x"))
fig.write_image(here / "slack.png", scale=2); fig.write_image(here / "slack.pdf")

# 2. the effect of C
Cs = [1000, 1, 0.05]
titles = []
for C in Cs:
    w, b = fit(C)
    pred = np.sign(X @ w + b)
    titles.append(f"C = {C:g}: margin {2 / np.linalg.norm(w):.2f}, {int((pred != y).sum())} mistake{'' if (pred != y).sum() == 1 else 's'}")
    print(titles[-1], "points with xi > 0:", int((xi(w, b) > 1e-6).sum()))
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05, subplot_titles=titles)
for k, C in enumerate(Cs, start=1):
    w, b = fit(C)
    draw(fig, w, b, row=1, col=k)
    wrong = np.sign(X @ w + b) != y
    fig.add_trace(go.Scatter(x=X[wrong, 0], y=X[wrong, 1], mode="markers", showlegend=False,
                             marker=dict(size=26, color="rgba(0,0,0,0)", line=dict(color="black", width=2.5))), 1, k)
fig.update_xaxes(title="x₁", **axes)
fig.update_yaxes(range=[0, 10])
fig.update_yaxes(title="x₂", row=1, col=1)
for k in (1, 2, 3):
    fig.update_yaxes(scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_layout(template="simple_white", width=980, height=420, font=font, margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=17)
fig.write_image(here / "c_effect.png", scale=2); fig.write_image(here / "c_effect.pdf")

# 3. hinge loss vs log loss, as functions of z = y (w.x + b)
z = np.linspace(-3, 3, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=z, y=np.maximum(0, 1 - z), mode="lines", name="hinge loss: max(0, 1 − z)",
                         line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=z, y=np.log(1 + np.exp(-z)), mode="lines", name="log loss: log(1 + e⁻ᶻ)",
                         line=dict(color=ORANGE, width=4, dash="dash")))
fig.add_vrect(x0=0, x1=1, fillcolor=GREY, opacity=0.12, line_width=0)
fig.add_annotation(x=0.5, y=3.6, text="inside the<br>margin", showarrow=False, font=dict(size=16, color=GREY))
fig.add_annotation(x=-1.8, y=3.6, text="wrong side", showarrow=False, font=dict(size=16, color=GREY))
fig.add_annotation(x=2.1, y=3.6, text="beyond its<br>own hyperplane", showarrow=False, font=dict(size=16, color=GREY))
fig.update_layout(template="simple_white", width=640, height=400, font=font, margin=dict(l=60, r=20, t=30, b=60),
                  legend=dict(x=0.98, xanchor="right", y=0.62),
                  xaxis=dict(title="z = y (wᵀx + b)", range=[-3, 3]), yaxis=dict(title="loss of one point", range=[0, 4.1]))
fig.write_image(here / "hinge.png", scale=2); fig.write_image(here / "hinge.pdf")
