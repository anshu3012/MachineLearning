"""Why a likelihood is not a probability (Plotly). Left: with p = 0.5 fixed, the binomial probabilities of 0 to 5
heads add up to 1. Right: with five heads fixed, the likelihood L(p) = p^5 over p from 0 to 1 has area 1/6."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.integrate import quad
from gifkit import BLUE, FONT, GREEN, ORANGE

here = Path(__file__).parent
k = np.arange(6)
pm = stats.binom.pmf(k, 5, 0.5)
area = quad(lambda p: p ** 5, 0, 1)[0]
assert np.isclose(pm.sum(), 1) and np.isclose(area, 1 / 6)
fig = make_subplots(1, 2, horizontal_spacing=0.12,
                    subplot_titles=[f"p = 0.5 fixed: probabilities add to {pm.sum():.3f}", f"5 heads fixed: area under L(p) = {area:.3f}"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Bar(x=k, y=pm, marker_color=ORANGE, text=[f"{v:.3f}" for v in pm], textposition="outside",
                     textfont=dict(size=16)), 1, 1)
p = np.linspace(0, 1, 201)
fig.add_trace(go.Scatter(x=p, y=p ** 5, mode="lines", fill="tozeroy", fillcolor="rgba(84,162,75,0.3)", line=dict(color=GREEN, width=4)), 1, 2)
fig.add_annotation(x=0.72, y=0.08, text="area = 1/6", showarrow=False, font=dict(size=22, color=GREEN), row=1, col=2)
fig.update_xaxes(title="number of heads k", row=1, col=1)
fig.update_yaxes(title="P(k | p = 0.5)", range=[0, 0.4], row=1, col=1)
fig.update_xaxes(title="parameter p", row=1, col=2)
fig.update_yaxes(title="L(p | 5 heads)", range=[0, 1.05], row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "sums.png", scale=2)
