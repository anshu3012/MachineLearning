"""The multiplier as a price (Plotly frames). A factory buys labour (20 rupees an hour) and steel (2,000 rupees a
tonne); its revenue is R = 100 h^(2/3) s^(1/3). For each budget b the best plan is where a revenue contour touches
the budget line: h = b/30, s = b/6000. The best revenue M*(b) rises by lambda = 0.57 rupees per extra rupee of budget.
Numbers after Khan Academy, "Lagrange multiplier example, part 1" and "Meaning of Lagrange multiplier" (dollars there).
Run: python budget_slider.py -> budget_slider.gif, budget_slider_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import minimize_scalar
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
R = lambda h, s: 100 * h ** (2 / 3) * s ** (1 / 3)
best = lambda b: (b / 30, b / 6000)
Mstar = lambda b: R(*best(b))
LAM = (200 / 3) * (best(20000)[1] / best(20000)[0]) ** (1 / 3) / 20          # dR/dh = 20 lambda
# checks: the closed form is the true maximum on the budget line; lambda is the slope of M*(b)
num = minimize_scalar(lambda h: -R(h, (20000 - 20 * h) / 2000), bounds=(1, 999), method="bounded")
assert abs(num.x - 2000 / 3) < 0.5 and abs(-num.fun - Mstar(20000)) < 0.01
assert abs((Mstar(20001) - Mstar(20000)) - LAM) < 1e-4 and round(LAM, 2) == 0.57 and round(Mstar(20000)) == 11400
bs = list(range(10000, 30001, 2000))
h = np.linspace(40, 1600, 300)


def frame(b):
    hb, sb = best(b)
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                        subplot_titles=("plans: hours of labour and tonnes of steel", "best revenue against the budget"))
    fig.add_trace(go.Scatter(x=[0, b / 20, 0], y=[b / 2000, 0, 0], fill="toself", fillcolor="rgba(84,162,75,0.15)",
                             line=dict(color=GREEN, width=4)), row=1, col=1)
    for m, col, w in ((0.7, GREY, 1.5), (1.0, BLUE, 4), (1.3, GREY, 1.5)):                 # revenue contours
        M = m * Mstar(b)
        fig.add_trace(go.Scatter(x=h, y=(M / 100) ** 3 / h ** 2, line=dict(color=col, width=w)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[hb], y=[sb], mode="markers", marker=dict(size=16, color=RED)), row=1, col=1)
    fig.add_annotation(x=hb, y=sb, xref="x", yref="y", text=f"best plan: {hb:.0f} h, {sb:.1f} t", showarrow=False,
                       xanchor="left", xshift=12, yshift=14, font=dict(size=20, color=RED), bgcolor="white")
    fig.update_xaxes(title="labour h (hours)", range=[0, 1600], row=1, col=1)
    fig.update_yaxes(title="steel s (tonnes)", range=[0, 16], row=1, col=1)
    done = [x for x in bs if x <= b]
    fig.add_trace(go.Scatter(x=bs, y=[Mstar(x) for x in bs], line=dict(color="#CCCCCC", width=2, dash="dot")), row=1, col=2)
    fig.add_trace(go.Scatter(x=done, y=[Mstar(x) for x in done], mode="lines+markers", line=dict(color=ORANGE, width=4),
                             marker=dict(size=9)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[b], y=[Mstar(b)], mode="markers", marker=dict(size=16, color=RED)), row=1, col=2)
    fig.add_annotation(x=11000, y=16500, xref="x2", yref="y2", xanchor="left", showarrow=False, align="left",
                       font=dict(size=20, color=ORANGE), text=f"slope = λ = {LAM:.2f}<br>rupees of revenue<br>per extra rupee of budget")
    fig.update_xaxes(title="budget b (rupees)", range=[9000, 31000], row=1, col=2)
    fig.update_yaxes(title="best revenue R* (rupees)", range=[0, 19000], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=580, font=FONT, showlegend=False,
                      margin=dict(l=75, r=20, t=115, b=65),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"budget b = {b:,} rupees: the budget line (green) moves out<br>"
                                      f"best revenue R* = <b>{Mstar(b):,.0f}</b> rupees"))
    fig.update_annotations(selector=dict(yref="paper"), font_size=20)
    return fig


figs = [frame(b) for b in bs]
holds = [8 if b in (10000, 20000) else 14 if b == 30000 else 3 for b in bs]
make_gif(figs, here / "budget_slider", fps=6, holds=holds, keys=[0, bs.index(20000), len(bs) - 1], cols=1, width=1000)
