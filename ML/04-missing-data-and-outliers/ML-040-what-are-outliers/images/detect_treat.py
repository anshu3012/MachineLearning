"""Detect, then treat, on the 714 known Titanic ages: (1) the ages; (2) detection: the IQR fences
Q1 - 1.5 IQR and Q3 + 1.5 IQR (-6.69 and 64.81); (3) the 11 ages above the upper fence are outliers; (4) treatment by
capping: they move onto the fence. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREEN

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_age.csv").Age.values
q1, q3 = np.percentile(age, [25, 75])
lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
out = age > hi
assert len(age) == 714 and round(hi, 2) == 64.81 and out.sum() == 11 and (age < lo).sum() == 0
jit = np.random.default_rng(0).uniform(-1, 1, len(age))
STEPS = ["714 Titanic ages", f"<b>detect</b>: IQR fences at {lo:.2f} and {hi:.2f}",
         f"{out.sum()} ages above the upper fence are outliers", f"<b>treat</b> by capping: the {out.sum()} outliers move to {hi:.2f}"]


def frame(k):
    v = np.where(out, hi, age) if k == 3 else age
    col = np.where(out & (k >= 2), RED if k == 2 else GREEN, BLUE)
    fig = go.Figure()
    if k >= 1:
        for f in (lo, hi):
            fig.add_vline(x=f, line=dict(color="black", width=3, dash="dash"))
    fig.add_scatter(x=v, y=jit, mode="markers", marker=dict(size=7, color=col, opacity=0.7))
    fig.update_layout(template="simple_white", width=1100, height=380, font=FONT, showlegend=False,
                      title=dict(text=STEPS[k], x=0.5), xaxis=dict(title="age (years)", range=[-10, 85]),
                      yaxis=dict(visible=False, range=[-1.4, 1.4]), margin=dict(l=30, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(4)], "detect_treat", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6], width=900)
