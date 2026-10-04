"""The chain rule as rates that multiply (Plotly), for h(x) = (x^2 + 1)^3 at x = 1. Three number lines: x, the
inside u = x^2 + 1, and the outside h = u^3. A nudge of 0.01 in x becomes a nudge of about 0.02 in u (rate 2) and
about 0.24 in h (rate 12 on top of that): 12 x 2 = 24. Drawn with each nudge magnified on its own line.
After Sanderson (3Blue1Brown), "Visualizing the chain rule and product rule"; our own numbers."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE

here = Path(__file__).parent
dx = 0.01
x0, u0 = 1.0, 2.0
du = (x0 + dx) ** 2 + 1 - u0
dh = ((x0 + dx) ** 2 + 1) ** 3 - u0 ** 3
assert round(du, 2) == 0.02 and round(dh, 2) == 0.24 and round(dh / dx) == 24
rows = [(2, "x", x0, dx, BLUE, f"nudge dx = {dx}"), (1, "u = x² + 1", u0, du, GREEN, f"du ≈ {du:.3f} = 2 × dx"),
        (0, "h = u³", u0 ** 3, dh, ORANGE, f"dh ≈ {dh:.3f} = 12 × du = 24 × dx")]
fig = go.Figure()
SCALE = 22                                    # draw each line with the nudge magnified around its point
for y, name, v, d, c, text in rows:
    fig.add_shape(type="line", x0=-1, x1=9, y0=y, y1=y, line=dict(color=GREY, width=2))
    fig.add_annotation(x=-1, y=y, text=f"<b>{name}</b>", showarrow=False, xanchor="right", xshift=-8, font=dict(size=20))
    fig.add_shape(type="rect", x0=0, x1=d * SCALE, y0=y - 0.08, y1=y + 0.08, fillcolor=c, line=dict(width=0), opacity=0.8)
    fig.add_annotation(x=0, y=y, text=f"{v:g}", showarrow=False, yshift=-22, font=dict(size=16))
    fig.add_annotation(x=d * SCALE if y > 0 else 0, y=y, text=text, showarrow=False, xanchor="left", xshift=10, yshift=0 if y > 0 else 30, font=dict(size=20, color=c))
for y in (2, 1):
    fig.add_annotation(x=-0.3, y=y - 0.85, ax=-0.3, ay=y - 0.15, xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                       arrowwidth=2, arrowcolor=GREY)
fig.add_annotation(x=-0.15, y=1.5, text="× 2  (inner rate: 2x at x = 1)", showarrow=False, xanchor="left",
                   font=dict(size=18, color=GREY))
fig.add_annotation(x=-0.15, y=0.5, text="× 12  (outer rate: 3u² at u = 2)", showarrow=False, xanchor="left",
                   font=dict(size=18, color=GREY))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, showlegend=False,
                  xaxis=dict(visible=False, range=[-2.6, 9]), yaxis=dict(visible=False, range=[-0.4, 2.5]),
                  margin=dict(l=20, r=20, t=20, b=20))
fig.write_image(here / "chain_rates.png", scale=2)
