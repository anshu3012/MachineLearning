"""AdaGrad on the sparse-feature loss: the effective learning rate eta / sqrt(v_t) of m and b over 500 steps (left),
and the distance to the minimum for eta = 2 and eta = 0.5 (right) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, GREEN, ORANGE, FONT
from shared import START, BEST, grad, run

here = Path(__file__).parent
p, s, eff = START.copy(), np.zeros(2), []
for _ in range(500):
    g = grad(p)
    s = s + g ** 2
    eff.append(2.0 / np.sqrt(s))
    p = p - 2.0 * g / (np.sqrt(s) + 1e-8)
eff = np.array(eff)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("effective learning rate, η = 2", "distance to the minimum"))
steps = np.arange(1, 501)
fig.add_trace(go.Scatter(x=steps, y=eff[:, 0], name="m (sparse IIT feature)", line=dict(color=GREEN, width=3)), 1, 1)
fig.add_trace(go.Scatter(x=steps, y=eff[:, 1], name="b (bias)", line=dict(color=BLUE, width=3)), 1, 1)
for eta, c, dash in ((2.0, GREEN, "solid"), (0.5, ORANGE, "solid")):
    P = run("adagrad", eta)
    fig.add_trace(go.Scatter(x=np.arange(501), y=np.linalg.norm(P - BEST, axis=1), name=f"AdaGrad, η = {eta:g}",
                             line=dict(color=c, width=3, dash=dash)), 1, 2)
fig.update_yaxes(title_text="η / √v<sub>t</sub>", range=[0, 0.65], row=1, col=1)
fig.update_yaxes(type="log", exponentformat="power", title_text="distance from (m, b) to the minimum", row=1, col=2)
fig.update_xaxes(title_text="step")
fig.update_layout(template="simple_white", width=1050, height=450, font=FONT,
                  showlegend=False, margin=dict(l=80, r=20, t=40, b=60))
for text, x, y, c, col in (("m (sparse IIT feature)", 250, eff[250, 0], GREEN, 1), ("b (bias)", 250, eff[250, 1], BLUE, 1)):
    fig.add_annotation(x=x, y=y, yshift=14, text=text, showarrow=False, font=dict(color=c), row=1, col=col)
for eta, c in ((2.0, GREEN), (0.5, ORANGE)):
    P = run("adagrad", eta)
    d = np.linalg.norm(P - BEST, axis=1)
    fig.add_annotation(x=250, y=np.log10(d[250]), yshift=16, text=f"AdaGrad, η = {eta:g}", showarrow=False,
                       font=dict(color=c), row=1, col=2)
fig.write_image(here / "effective_lr.png", scale=2)
fig.write_image(here / "effective_lr.pdf")
