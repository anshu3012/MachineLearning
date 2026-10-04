"""Normalization removes the units: the Note's five weights written in grams, kilograms and pounds have very
different numbers, but min-max scaling turns all three into the same five values."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
kg = np.array([130, 60, 67, 32, 54.0])
units = {"kilograms": kg, "grams": kg * 1000, "pounds": kg * 2.20462}
mm = lambda v: (v - v.min()) / (v.max() - v.min())
for v in units.values():
    assert np.allclose(mm(v), [1, 0.2857, 0.3571, 0, 0.2245], atol=1e-4)
POS = ["top center", "bottom center", "top center", "top center", "top center"]   # 130, 60, 67, 32, 54
COL = ["#E45756", "#4C78A8", "#F58518", "#54A24B", "#B279A2"]
fig = make_subplots(rows=2, cols=3, vertical_spacing=0.25, horizontal_spacing=0.06,
                    subplot_titles=[f"in {u}" for u in units] + ["after min-max scaling"] * 3)
for j, (u, v) in enumerate(units.items(), start=1):
    fig.add_scatter(x=v, y=[0] * 5, mode="markers+text", marker=dict(size=18, color=COL), text=[f"{x:,.0f}" for x in v],
                    textposition=POS, textfont=dict(size=14), row=1, col=j)
    fig.add_scatter(x=mm(v), y=[0] * 5, mode="markers+text", marker=dict(size=18, color=COL),
                    text=[f"{x:.2f}" for x in mm(v)], textposition=POS, textfont=dict(size=14), row=2, col=j)
    fig.update_xaxes(range=[-0.1, 1.1], row=2, col=j)
    fig.update_xaxes(range=[v.min() - 0.12 * np.ptp(v), v.max() + 0.12 * np.ptp(v)], row=1, col=j)
fig.update_yaxes(visible=False, range=[-1.2, 1.2])
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1600, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=20, r=20, t=50, b=40))
fig.write_image(here / "units.png", scale=2)
fig.write_image(here / "units.pdf")
