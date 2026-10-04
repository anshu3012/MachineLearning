"""Sample skewness of 1, 2, 3, 4, 10 step by step: standardize (mean 4, s = 3.536), cube, add up (4.074), multiply
by 5 / (4 x 3): G1 = 1.70, the same as pandas. Cubing keeps the sign and makes the far value 10 dominate.
Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
x = np.array([1, 2, 3, 4, 10.0])
m, s = x.mean(), x.std(ddof=1)
z = (x - m) / s
c = z ** 3
G1 = len(x) / ((len(x) - 1) * (len(x) - 2)) * c.sum()
assert round(s, 3) == 3.536 and round(c.sum(), 3) == 4.073 and round(G1, 2) == 1.70 == round(pd.Series(x).skew(), 2)
STEPS = [(x - m, "Step 1: distance from the mean 4", "x − x̄", [-4, 7]),
         (z, "Step 2: divide by s = 3.536 (standardize)", "z", [-1.5, 5.4]),
         (c, f"Step 3: cube. Sum = {c.sum():.3f}", "z³", [-1.5, 5.4]),
         (c, f"Step 4: G<sub>1</sub> = 5 / (4 × 3) × {c.sum():.3f} = <b>{G1:.2f}</b>", "z³", [-1.5, 5.4])]


def frame(v, head, lab, yr):
    fig = go.Figure(go.Bar(x=[f"x = {int(a)}" for a in x], y=v, marker_color=[RED if a < 0 else BLUE for a in v],
                           text=[f"{a:.3f}" for a in v], textposition="outside", textfont=dict(size=22)))
    fig.add_hline(y=0, line=dict(color="black", width=1))
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), yaxis=dict(title=lab, range=yr),
                      margin=dict(l=90, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(*st) for st in STEPS], "cube_steps", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6])
