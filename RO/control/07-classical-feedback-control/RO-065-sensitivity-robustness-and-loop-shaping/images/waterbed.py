"""The waterbed effect (Bode's integral formula) on the heading loop. The natural logarithm of |S| is drawn against
frequency on a LINEAR axis, for the lead alone (purple, dashed) and the lead-lag (green). For a loop with no unstable
poles whose gain falls at least as fast as 1/w^2, the area below zero equals the area above zero. Lead alone:
-3.22 and +3.22; lead-lag: -3.45 and +3.45 (1.18 of it lies beyond 15 rad/s, off the chart). Pushing |S| down at low
frequencies has pushed it up above 1.90 rad/s. Run: python waterbed.py -> waterbed.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.integrate import quad
from scipy.optimize import brentq
from gifkit import FONT, GREEN, GREY, PURPLE, RED
from loopkit import C_lead, C_leadlag, P_head

here = Path(__file__).parent


def lnS(C):
    return lambda x: np.log(abs(1 / (1 + C(1j * x) * P_head(1j * x))))


areas = {}
for name, C in (("lead", C_lead), ("leadlag", C_leadlag)):
    f = lnS(C)
    wsc = brentq(f, 0.5, 5)
    neg = quad(f, 0, wsc, limit=500, points=[0.025, 0.25, 0.833])[0]
    pos = sum(quad(f, lo, hi, limit=500)[0] for lo, hi in ((wsc, 15), (15, 1e3), (1e3, 1e6)))
    areas[name] = (wsc, neg, pos)
    assert abs(neg + pos) < 1e-3
assert abs(areas["lead"][1] + 3.22) < 5e-3 and abs(areas["leadlag"][1] + 3.45) < 5e-3 and abs(areas["leadlag"][0] - 1.90) < 5e-3

w = np.linspace(1e-4, 15, 3000)
y = lnS(C_leadlag)(w)
yl = lnS(C_lead)(w)
fig = go.Figure()
fig.add_trace(go.Scatter(x=w, y=np.minimum(y, 0), fill="tozeroy", fillcolor="rgba(84,162,75,0.25)", mode="none",
                         showlegend=False))
fig.add_trace(go.Scatter(x=w, y=np.maximum(y, 0), fill="tozeroy", fillcolor="rgba(228,87,86,0.25)", mode="none",
                         showlegend=False))
fig.add_trace(go.Scatter(x=w, y=yl, line=dict(color=PURPLE, width=4, dash="dash"), name="lead alone"))
fig.add_trace(go.Scatter(x=w, y=y, line=dict(color=GREEN, width=5), name="lead-lag"))
fig.add_hline(y=0, line=dict(color=GREY, width=2))
fig.add_annotation(x=0.35, y=-2.0, text="area below 0 (down to −∞ at ω = 0):<br>lead −3.22, lead-lag −3.45",
                   ax=210, ay=0, xanchor="left", font=dict(size=19, color=GREEN), arrowcolor=GREEN)
fig.add_annotation(x=9, y=0.75, text="area above 0 (out to ω = ∞):<br>lead +3.22, lead-lag +3.45", showarrow=False,
                   font=dict(size=19, color=RED))
fig.update_xaxes(title_text="frequency ω (rad/s), linear scale", range=[0, 15])
fig.update_yaxes(title_text="ln |S|  (natural logarithm)", range=[-4.5, 1.2])
fig.update_layout(template="simple_white", font=FONT, width=1000, height=650, margin=dict(l=90, r=30, t=110, b=70),
                  legend=dict(x=0.6, y=0.2, font=dict(size=18)),
                  title=dict(x=0.5, y=0.97, text="the waterbed: the area below zero equals the area above"))
fig.write_image(here / "waterbed.png", scale=1)
