"""How outliers spoil a linear regression, on example data: 20 students whose marks rise with study hours, then the
same 20 plus two students with very few hours and top marks. The least-squares line tilts toward the two, and its
error on the 20 ordinary students grows. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
rng = np.random.default_rng(1)
h = rng.uniform(2, 20, 20)
m = 30 + 3 * h + rng.normal(0, 5, 20)
oh, om = np.array([2.5, 3.5]), np.array([96.0, 93.0])
fit = lambda x, y: np.polyfit(x, y, 1)
p0, p1 = fit(h, m), fit(np.r_[h, oh], np.r_[m, om])
mae = lambda p: np.mean(np.abs(np.polyval(p, h) - m))
assert p1[0] < p0[0] and mae(p1) > mae(p0)


def frame(k):
    fig = go.Figure()
    g = np.array([0, 22])
    fig.add_scatter(x=g, y=np.polyval(p0, g), mode="lines", line=dict(color=BLUE, width=3, dash="dash" if k else "solid"))
    if k:
        fig.add_scatter(x=g, y=np.polyval(p1, g), mode="lines", line=dict(color=RED, width=4))
        fig.add_scatter(x=oh, y=om, mode="markers", marker=dict(size=18, color=RED, symbol="x"))
    fig.add_scatter(x=h, y=m, mode="markers", marker=dict(size=12, color=BLUE))
    p = p1 if k else p0
    head = (f"20 students: slope {p0[0]:.2f} marks per hour, average error {mae(p0):.1f} marks" if not k else
            f"+ 2 outliers: slope {p1[0]:.2f}, average error on the 20 students {mae(p1):.1f} marks")
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, font=dict(size=21)), xaxis=dict(title="study hours per week (example data)", range=[0, 22]),
                      yaxis=dict(title="marks", range=[20, 105]), margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(0), frame(1)], "study_marks", here, keys=[0, 1], fps=1, holds=[4, 6])
