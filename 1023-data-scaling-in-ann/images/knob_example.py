"""Section 4.1's worked example as bars (log scale): the gradient of each weight is delta times its input,
and the same Adam-sized step moves z far more through salary than through age (Plotly)."""
from pathlib import Path
from plotly.subplots import make_subplots
from common import ORANGE, PURPLE, FONT

here = Path(__file__).parent
delta, age, salary = 0.01, 40, 80_000
g = [delta * age, delta * salary]
assert g == [0.4, 800] and g[1] / g[0] == 2000
step, mean_age, mean_sal = 0.004, 38, 70_000                       # first-epoch weight change, typical inputs
dz = [step * mean_age, step * mean_sal]
assert round(dz[0], 2) == 0.15 and dz[1] == 280
fig = make_subplots(1, 2, horizontal_spacing=0.14,
                    subplot_titles=["Gradient = δ × input (δ = 0.01)", "Shift in z from a 0.004 step"])
labels = ["age (40)", "salary (80,000)"]
fig.add_bar(x=labels, y=g, marker_color=[ORANGE, PURPLE], text=["0.4", "800"], textposition="outside",
            showlegend=False, row=1, col=1)
fig.add_bar(x=["through age", "through salary"], y=dz, marker_color=[ORANGE, PURPLE], text=["0.15", "280"],
            textposition="outside", showlegend=False, row=1, col=2)
fig.update_yaxes(type="log", range=[-1.3, 3.6], title="log scale", tickvals=[0.1, 1, 10, 100, 1000])
fig.update_layout(template="simple_white", width=1050, height=460, font=dict(FONT, size=18),
                  margin=dict(l=70, r=20, t=50, b=50))
fig.update_annotations(font_size=19)
fig.write_image(here / "knob_example.png", scale=2)
fig.write_image(here / "knob_example.pdf")
