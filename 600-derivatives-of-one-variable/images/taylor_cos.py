"""Building the Taylor polynomial of cos x at 0 one coefficient at a time (Plotly frames): match the value (c0 = 1),
the slope (c1 = 0), the bend (c2 = -1/2), then add the x^4 / 24 term. Check: 1 - 0.1^2 / 2 = 0.995 = cos 0.1 to 3 places.
Idea after 3Blue1Brown, "Taylor series". Run: python taylor_cos.py -> taylor_cos.gif, taylor_cos_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
assert round(1 - 0.1 ** 2 / 2, 3) == round(float(np.cos(0.1)), 3) == 0.995
x = np.linspace(-4.5, 4.5, 400)
TICK, TODO = "✓", "·"


def frame(c2, c4, done, title, formula):
    """done: how many of value / slope / bend are matched so far."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=np.cos(x), line=dict(color="black", width=4)))
    fig.add_trace(go.Scatter(x=x, y=1 + c2 * x ** 2 + c4 * x ** 4, line=dict(color=ORANGE, width=4, dash="dash")))
    fig.add_trace(go.Scatter(x=[0], y=[1], mode="markers", marker=dict(size=14, color=GREEN)))
    for i, name in enumerate(("value: cos 0 = 1", "slope: 0", "bend: −1")):
        ok = i < done
        fig.add_annotation(x=-1.3, y=2.25 - 0.3 * i, xanchor="left", showarrow=False,
                           text=f"{TICK if ok else TODO} {name}", font=dict(size=22, color=GREEN if ok else GREY))
    fig.add_annotation(x=0, y=-1.15, showarrow=False, text=formula,
                       font=dict(size=24, color=ORANGE), bgcolor="white")
    fig.add_annotation(x=3.14, y=-1.25, text="cos x", showarrow=False, font=dict(size=22))
    fig.update_xaxes(title="x", range=[-4.5, 4.5], zeroline=True, zerolinecolor="#DDDDDD")
    fig.update_yaxes(range=[-1.6, 2.5], zeroline=True, zerolinecolor="#DDDDDD")
    fig.update_layout(template="simple_white", width=900, height=600, font=FONT, showlegend=False,
                      margin=dict(l=60, r=20, t=70, b=65), title=dict(text=title, x=0.5, font=dict(size=23)))
    return fig


figs = [frame(0, 0, 1, "Step 1. Match the value: c₀ = 1", "T(x) = 1"),
        frame(0, 0, 2, "Step 2. Match the slope: c₁ = 0, the line stays flat", "T(x) = 1 + 0·x")]
c2s = [-0.1, -0.2, -0.3, -0.4, -0.5]
figs += [frame(c, 0, 2, "Step 3. Bend the parabola until it curves like cos x", f"T(x) = 1 − {abs(c):.1f}·x²") for c in c2s]
figs.append(frame(-0.5, 0, 3, "Step 3. Match the bend: 2c₂ = −1, so c₂ = −½", "T(x) = 1 − x²/2<br>T(0.1) = 0.995"))
c4s = [1 / 96, 1 / 48, 1 / 32, 1 / 24]
figs += [frame(-0.5, c, 3, "Step 4. Add an x⁴ term: it hugs cos x for longer", "T(x) = 1 − x²/2 + c₄·x⁴") for c in c4s[:-1]]
figs.append(frame(-0.5, 1 / 24, 3, "Step 4. Fourth derivative: 24·c₄ = 1, so c₄ = 1/24", "T(x) = 1 − x²/2 + x⁴/24"))
holds = [9, 9, 2, 2, 2, 2, 2, 12, 2, 2, 2, 14]
make_gif(figs, here / "taylor_cos", fps=6, holds=holds, keys=[0, 1, 7, len(figs) - 1])
