"""Anatomy of the normal curve: heights of adult men, N(68, 3) inches. Mean = median = mode at the centre,
mirror-image halves, tails that approach the x axis without touching it."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
ORANGE, BLUE, GREY = "#F58518", "#4C78A8", "#6B6B6B"
mu, sd = 68, 3
d = stats.norm(mu, sd)
x = np.linspace(56, 80, 600)
fig = go.Figure()
fig.add_scatter(x=x, y=d.pdf(x), mode="lines", line=dict(color=ORANGE, width=4), fill="tozeroy",
                fillcolor="rgba(245,133,24,0.12)")
fig.add_shape(type="line", x0=mu, x1=mu, y0=0, y1=d.pdf(mu), line=dict(color=GREY, width=2, dash="dash"))
fig.add_annotation(x=mu, y=d.pdf(mu), text="mean = median = mode = 68", ax=0, ay=-35, font=dict(size=18))
for side, xx in (("left", 58), ("right", 78)):
    fig.add_annotation(x=xx, y=d.pdf(xx), text="tail: comes ever closer to 0,<br>never touches the axis",
                       ax=70 if side == "left" else -70, ay=-80, font=dict(size=16), arrowcolor=GREY)
fig.add_annotation(x=65.5, y=0.04, text="mirror<br>image", showarrow=False, font=dict(size=17, color=BLUE))
fig.add_annotation(x=70.5, y=0.04, text="mirror<br>image", showarrow=False, font=dict(size=17, color=BLUE))
fig.add_annotation(x=74.5, y=0.115, text="many values near the centre,<br>fewer and fewer far away",
                   showarrow=False, font=dict(size=16, color=GREY))
fig.update_layout(template="simple_white", width=1000, height=440, showlegend=False,
                  xaxis=dict(title="height of an adult man (inches)", dtick=3, range=[56, 80]),
                  yaxis=dict(title="density f(x)", range=[0, 0.16]),
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=20, b=50))
fig.write_image(here / "bell_anatomy.png", scale=2)
fig.write_image(here / "bell_anatomy.pdf")
