"""Why a ratio is a useful constructed feature, on illustrative numbers: two batters both score 45 runs, one off 30
balls and one off 45. Raw runs call them equal; strike rate = runs / balls x 100 separates them (150 against 100)."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
B = {"batter A": (45, 30), "batter B": (45, 45)}
sr = {k: r / b * 100 for k, (r, b) in B.items()}
assert sr["batter A"] == 150 and sr["batter B"] == 100
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=["raw feature: runs (the same)", "constructed feature: strike rate"])
fig.add_bar(x=list(B), y=[r for r, _ in B.values()], marker_color="#9a9a9a", text=[f"{r} runs" for r, _ in B.values()],
            textposition="outside", row=1, col=1)
fig.add_bar(x=list(B), y=list(sr.values()), marker_color=["#F58518", "#4C78A8"],
            text=[f"{r}/{b} × 100 = {s:g}" for (r, b), s in zip(B.values(), sr.values())], textposition="outside", row=1, col=2)
fig.update_yaxes(range=[0, 60], title_text="runs", row=1, col=1)
fig.update_yaxes(range=[0, 185], title_text="runs per 100 balls", row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 20
fig.update_layout(template="simple_white", width=1100, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=60, b=50))
fig.write_image(here / "ratio_feature.png", scale=2)
fig.write_image(here / "ratio_feature.pdf")
