"""Reading a correlation: 60 points whose correlation is swept from -1 to +1. The same random draws are reused in
every frame, so only the strength of the straight-line relationship changes. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREY

here = Path(__file__).parent
rng = np.random.default_rng(7)
a, b = rng.standard_normal(60), rng.standard_normal(60)
a = (a - a.mean()) / a.std()
b = b - a * (a @ b) / (a @ a); b = (b - b.mean()) / b.std()          # b exactly uncorrelated with a
TARGETS = [-1, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1]


def frame(rho):
    y = rho * a + np.sqrt(1 - rho ** 2) * b
    r = np.corrcoef(a, y)[0, 1]
    assert np.isclose(r, rho)
    c = BLUE if r > 0.05 else (RED if r < -0.05 else GREY)
    words = {1: "perfect rising line", 0.9: "strong", 0.6: "moderate", 0.3: "weak", 0: "no straight-line relationship"}[abs(rho)]
    fig = go.Figure(go.Scatter(x=a, y=y, mode="markers", marker=dict(size=12, color=c, line=dict(color="white", width=1))))
    fig.update_layout(template="simple_white", width=800, height=760, font=FONT, showlegend=False,
                      title=dict(text=f"<b>r = {'0' if abs(r) < 1e-9 else format(r, '+.1f')}</b>: {words if rho >= 0 or rho == 0 else words.replace('rising', 'falling')}", x=0.5),
                      xaxis=dict(range=[-3.2, 3.2], title="x (standardized)"),
                      yaxis=dict(range=[-3.2, 3.2], title="y (standardized)", scaleanchor="x"),
                      margin=dict(l=80, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(t) for t in TARGETS], "r_sweep", here, keys=[0, 2, 4, 6, 7, 8], fps=1, cols=3,
             holds=[3] + [2] * 7 + [5], width=640)
