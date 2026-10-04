"""Shadow prices of the workshop, re-solved (Plotly): best profit with the original limits (11) and with one more
unit of each resource: oven 13, flour 11, demand 12. The rises, 2, 0 and 1, are the multipliers."""
from pathlib import Path
import plotly.graph_objects as go
from scipy.optimize import linprog
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE

here = Path(__file__).parent
A, b = [[1, 1], [1, 3], [1, 0]], [4, 9, 3]
best = lambda bb: -linprog([-3, -2], A_ub=A, b_ub=bb, bounds=[(0, None)] * 2).fun
base = best(b)
rows = [("oven +1 hour", [5, 9, 3]), ("flour +1 bag", [4, 10, 3]), ("demand +1 batch", [4, 9, 4])]
vals = [best(bb) for _, bb in rows]
assert round(base, 6) == 11 and [round(v, 6) for v in vals] == [13, 11, 12]
fig = go.Figure(go.Bar(x=["original limits"] + [r[0] for r in rows], y=[base] + vals,
                       marker_color=[GREY, ORANGE, BLUE, GREEN],
                       text=[f"{base:.0f}"] + [f"{v:.0f} (λ = {v - base:.0f})" for v in vals], textposition="outside",
                       textfont=dict(size=21)))
fig.add_hline(y=base, line=dict(color=GREY, dash="dash", width=2), opacity=1)
fig.update_layout(template="simple_white", width=950, height=520, font=FONT, showlegend=False,
                  yaxis=dict(title="best profit (thousand rupees)", range=[0, 15]), margin=dict(l=80, r=30, t=20, b=60))
fig.write_image(here / "shadow_bars.png", scale=2)
