"""Section 5's worked example: three stumps vote -1, +1, -1 with alphas 2, 10 and 1; the weighted votes -2, +10, -1
add up to +7, so the prediction is +1 (placed). Plotly waterfall."""
from pathlib import Path
import plotly.graph_objects as go
from adaboost_common import BLUE, ORANGE, GREEN, FONT

here = Path(__file__).parent
votes, alphas = [-1, 1, -1], [2, 10, 1]
parts = [a * v for a, v in zip(alphas, votes)]
assert parts == [-2, 10, -1] and sum(parts) == 7
fig = go.Figure(go.Waterfall(
    x=["stump 1<br>h = -1, α = 2", "stump 2<br>h = +1, α = 10", "stump 3<br>h = -1, α = 1", "total"],
    measure=["relative", "relative", "relative", "total"], y=parts + [0],
    text=["-2", "+10", "-1", "+7: sign +1, placed"], textposition="outside",
    increasing=dict(marker=dict(color=BLUE)), decreasing=dict(marker=dict(color=ORANGE)), totals=dict(marker=dict(color=GREEN)),
    connector=dict(line=dict(color="#999999", dash="dot"))))
fig.add_hline(y=0, line=dict(color="black", width=1.5))
fig.update_layout(template="simple_white", width=1000, height=440, font=dict(FONT, size=19), showlegend=False,
                  yaxis=dict(title="running sum of α × h", range=[-4, 11]), margin=dict(l=80, r=20, t=20, b=80))
fig.write_image(here / "vote_example.png", scale=2)
fig.write_image(here / "vote_example.pdf")
