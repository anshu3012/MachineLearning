"""The loss over (m, b) of y = m x + b, for a dense feature (left) and the sparse IIT feature (right), as surfaces
tilting from the side view to the top view, which is the contour map of Figure 3 (sparse_bowl.py). Height = the loss;
the lines are at the contour map's own levels. Red path (right): gradient descent, eta = 0.3, from (-4, -4).
Run: python bowl_tilt.py -> bowl_tilt.gif, bowl_tilt_frames.png"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT
from shared import DATA, X as Xs, y as ys, run, loss
from surf import data_quad, quad_surface, BOWL_LEVELS, path3d, star3d, scene, phase, gif

HERE = Path(__file__).parent
dn = pd.read_csv(DATA / "dense.csv")
SETS = ((np.c_[dn.x, np.ones(len(dn))], dn.y.to_numpy()), (Xs, ys))
START = np.array([-4.0, -4.0])
LO, HI, N = -0.6, 2.4, 24
P = run("gd", 0.3, steps=45)
ZMAX = 80                                                   # the walls go higher than drawn
panels = []
for X, y in SETS:
    best, H, lmin = data_quad(X, y)
    m, b = np.linspace(best[0] - 10, best[0] + 10, 90), np.linspace(best[1] - 10, best[1] + 10, 90)
    panels.append((m, b, quad_surface(m, b, best, H, lmin, BOWL_LEVELS, ZMAX, LO, HI), best, lmin))
height = lambda p: loss(p)


def frame(k):
    t = k / (N - 1)
    fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "scene"}]], horizontal_spacing=0.0,
                        subplot_titles=("dense feature: round bowl", "sparse feature (90% zeros): elongated bowl"))
    for i, (m, b, tr, best, lmin) in enumerate(panels, start=1):
        sc = f"scene{i}" if i > 1 else "scene"
        for tt in tr:
            tt.scene = sc
            fig.add_trace(tt, 1, i)
        fig.add_trace(star3d(best[0], best[1], lmin + 0.4, scene=sc), 1, i)
    fig.add_trace(path3d(P, np.minimum(np.array([height(p) for p in P]), ZMAX), scene="scene2"), 1, 2)
    kw = dict(zr=[LO, HI], aspect=(1.2, 1.2, 0.8), t=t)
    for i, (m, b, *_r) in enumerate(panels, start=1):
        fig.layout[f"scene{i}" if i > 1 else "scene"].update(
            scene("m", "b", "loss L", [0, ZMAX], kw["aspect"], t, x=dict(range=[m[0], m[-1]], nticks=4),
                  y=dict(range=[b[0], b[-1]], nticks=4), z=dict(nticks=3)))
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=18),
                      title=dict(text=phase(t), x=0.5, y=0.985), margin=dict(l=0, r=0, t=90, b=0))
    return fig


if __name__ == "__main__":
    gif(HERE, "bowl_tilt", frame, N, 3, 8, 6, 900, (0, 8, 16, N - 1))
